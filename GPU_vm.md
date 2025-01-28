# Install the GPU driver manually

After launch a Windows instance Standard_NV4as_v4, how to verify what is the GPU of it?

Method 1: Using Windows Device Manager
Expand the Display Adapters section. You should see the GPU listed here.
For Standard_NV4as_v4, you will typically see AMD Radeon Instinct MI25.
Method 2: Using DirectX Diagnostic Tool (dxdiag)
Run dxdiag: Go to the Display Tab:
Navigate to the Display 1 tab (or similar). It will show the GPU details, including name, memory, and driver version.
Method 3: Using Command Line (PowerShell/Command Prompt)
```Get-WmiObject Win32_VideoController | Select-Object Name, AdapterRAM```
This will show the GPU name and memory (RAM) information.

with method 1 and 3, I got only the following 2. Method 2 shows Unknown device and Unkown drivers
```
    Microsoft Hyper-V Video
    Microsoft Basic Display Adapter
```
This is because the [GPU drivers for the AMD Radeon Instinct MI25](https://learn.microsoft.com/en-us/azure/virtual-machines/windows/n-series-amd-driver-setup#nvv4-series) on your Standard_NV4as_v4 VM are not installed or configured properly

After installation, method 1 and 3 shows:
```
Microsoft Hyper-V Video
Radeon Instinct MI25 MxGPU 2080374784
```
Method 2 shows:
```
---------------
Display Devices
---------------
           Card name: Radeon Instinct MI25 MxGPU
        Manufacturer: Advanced Micro Devices, Inc.
           Chip type: AMD FirePro SDI (0x686C)
            DAC type: Internal DAC(400MHz)
         Device Type: Full Device
          Device Key: Enum\PCI\VEN_1002&DEV_686C&SUBSYS_0C351002&REV_00
       Device Status: 0180600A [DN_DRIVER_LOADED|DN_STARTED|DN_DISABLEABLE|DN_REMOVABLE|DN_NT_ENUMERATOR|DN_NT_DRIVER] 
 Device Problem Code: No Problem
 Driver Problem Code: Unknown
      Display Memory: 9135 MB
    Dedicated Memory: 1967 MB
       Shared Memory: 7167 MB
        Current Mode: 1920 x 1080 (32 bit) (32Hz)
```
This manual way is time consuming, Let's use ARM extension, refer to azure-template.json