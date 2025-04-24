// Environment variables
val = BuildConfig.IP_ADDR

class SystemMonitor {
    private val cpuUsage: Double
    private val memoryUsage: Double
    private val diskUsage: Double

    init {
        cpuUsage = getCpuUsage()
        memoryUsage = getMemoryUsage()
        diskUsage = getDiskUsage()
    }

    private fun getCpuUsage(): Int {
        try {
            val pid = android.os.Process.myPid().toString()
            val cores = Runtime.getRuntime().availableProcessors()
            val process = Runtime.getRuntime().exec("top -n 1 -o PID,%CPU")
            val bufferedReader = BufferedReader(InputStreamReader(process.inputStream))
            var line = bufferedReader.readLine()

            while (line != null) {
                if (line.contains(pid)) {
                    val rawCpu = line.split(" ").last().toInt()
                    return (rawCpu / cores) * 100.0
                }
                line = bufferedReader.readLine()
            }
        } catch (e: Exception) {
            return 0
        }

        return 0
    }

    private fun getMemoryUsage(): Double {
        MemoryInfo mi = new MemoryInfo();
        ActivityManager activityManager = (ActivityManager) getSystemService(ACTIVITY_SERVICE);

        activityManager.getMemoryInfo(mi);
        double availableMegs = mi.availMem / 0x100000L;

        //Percentage can be calculated for API 16+
        double percentAvail = mi.availMem / (double)mi.totalMem * 100.0;

        return percentAvail;
    }
}