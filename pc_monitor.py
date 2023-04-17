import subprocess
import time

"""This code is meant to run in the background to monitor the internal temperature and battery of the PC, giving 
warnings to the user, and shutting down when critical levels are met.

note: I couldn't use a list of strings with low_battery power for some reason using 'if battery in list'.

Also, since I only have a virtual machine for linux, inxi was not able to track the temperature of my actual pc. So
the first part is purely guessing based on the examples on the web. If ti does not work, the field number might be wher to look"""

def install_inxi():
    subprocess.run('sudo apt install inxi', shell=True)
def temp_check():
    temperature_output = subprocess.run('inxi -F | grep "cpu" | grep "temp" | cut -d " " -f 4', shell=True, capture_output=True, text=True)
    temperature = temperature_output.stdout
    temperature = temperature.rstrip()
    if temperature == '70' or temperature == '71' or temperature == '72':
        subprocess.run('echo "DEVICE IS GETTING HOT"', shell=True)
    if temperature =='80' or temperature == '81' or temperature == '82':
        subprocess.run('shutdown +5 "PC will shut down due to extensive heat temperatures in 5 minutes"', shell=True)
        #This will sleep the program so shutdown can proceed.
        time.sleep(350)
def battery_check():
    battery_output = subprocess.run('inxi -B | grep "charge" | cut -d " " -f 8 | cut -c 2-5', shell=True, capture_output=True, text=True)
    battery = battery_output.stdout
    battery = battery.rstrip()
    if battery == '15.0' or battery == '14.0' or battery == '13.0':
        print(f'Batter level at {battery}%')
        subprocess.run('echo "DEVICE IS LOW ON POWER, PLEASE PLUG IN DEVICE"', shell=True)
    elif battery == '12.0' or battery == '11.0' or battery == '10.0':
        subprocess.run('shutdown +5 "PC will shut down due to low power in 5 minutes"', shell=True)
        #This will sleep the program so shutdown can proceed.
        time.sleep(350)

def main():
    install_inxi()
    while True:
        battery_check()
        temp_check()
        #This program will run every 2 minutes
        time.sleep(120)
if __name__ == "__main__":
    main()

