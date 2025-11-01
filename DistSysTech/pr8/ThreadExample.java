package DistSysTech.pr8;

class indirectThread extends Thread {
    @Override
    public void run() {
        System.out.println("Side stream is being executed");
    }
}

public class ThreadExample {
    static indirectThread indirectThread;

    public static void main(String[] args) {
        indirectThread = new indirectThread();
        indirectThread.start();

        System.out.println("Main stream");
    }
}