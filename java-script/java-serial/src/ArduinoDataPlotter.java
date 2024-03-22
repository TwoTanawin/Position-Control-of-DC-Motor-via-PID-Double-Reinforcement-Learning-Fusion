import java.awt.Dimension;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.TooManyListenersException;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

import javax.swing.JFrame;
import javax.swing.SwingUtilities;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.data.xy.XYSeries;
import org.jfree.data.xy.XYSeriesCollection;
import gnu.io.*;


public class ArduinoDataPlotter extends JFrame implements SerialPortEventListener {
    private XYSeries series1;
    private XYSeries series2;
    private XYSeries series3;
    private SerialPort serialPort;

    public ArduinoDataPlotter() {
        super("Arduino Data Plotter");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // Create a dataset
        XYSeriesCollection dataset = new XYSeriesCollection();
        series1 = new XYSeries("Random Data 1");
        series2 = new XYSeries("Random Data 2");
        series3 = new XYSeries("Random Data 3");
        dataset.addSeries(series1);
        dataset.addSeries(series2);
        dataset.addSeries(series3);

        // Create the chart
        JFreeChart chart = ChartFactory.createXYLineChart(
                "Arduino Data Plot", "Time", "Value", dataset);

        // Create and set up the chart panel
        ChartPanel chartPanel = new ChartPanel(chart);
        chartPanel.setPreferredSize(new Dimension(800, 600));
        getContentPane().add(chartPanel);

        // Start a thread to fetch data from Arduino
        ScheduledExecutorService executor = Executors.newSingleThreadScheduledExecutor();
        executor.scheduleAtFixedRate(this::connectToArduino, 0, 1, TimeUnit.SECONDS);
    }

    private void connectToArduino() {
        CommPortIdentifier portIdentifier;
        try {
            portIdentifier = CommPortIdentifier.getPortIdentifier("/dev/ttyUSB0");
            if (portIdentifier.isCurrentlyOwned()) {
                System.out.println("Error: Port is currently in use");
            } else {
                CommPort commPort = portIdentifier.open(this.getClass().getName(), 2000);
                if (commPort instanceof SerialPort) {
                    serialPort = (SerialPort) commPort;
                    serialPort.setSerialPortParams(115200, SerialPort.DATABITS_8, SerialPort.STOPBITS_1, SerialPort.PARITY_NONE);
                    serialPort.addEventListener(this);
                    serialPort.notifyOnDataAvailable(true);
                } else {
                    System.out.println("Error: Only serial ports are handled by this example.");
                }
            }
        } catch (NoSuchPortException | PortInUseException | UnsupportedCommOperationException | TooManyListenersException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void serialEvent(SerialPortEvent event) {
        if (event.getEventType() == SerialPortEvent.DATA_AVAILABLE) {
            try {
                BufferedReader reader = new BufferedReader(new InputStreamReader(serialPort.getInputStream()));
                String line = reader.readLine();
                String[] values = line.split(",");
                if (values.length >= 3) {
                    int data1 = Integer.parseInt(values[0]);
                    int data2 = Integer.parseInt(values[1]);
                    int data3 = Integer.parseInt(values[2]);

                    SwingUtilities.invokeLater(() -> {
                        series1.addOrUpdate(series1.getItemCount(), data1);
                        series2.addOrUpdate(series2.getItemCount(), data2);
                        series3.addOrUpdate(series3.getItemCount(), data3);
                    });
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            ArduinoDataPlotter plotter = new ArduinoDataPlotter();
            plotter.pack();
            plotter.setVisible(true);
        });
    }
}
