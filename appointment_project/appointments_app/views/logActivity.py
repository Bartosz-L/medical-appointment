import os


# modił przeprowadza logowanie aktywności poprzez zapis logów do pliku textowego,
# który póżniej jest renderowany w HTMLu dla administratora do wglądu
def logActivity(activity):
    filename = "log.txt"
    cwd = os.getcwd()
    target = open(cwd + "\\appointments_app\\log\\" + filename, 'a')
    target.write(activity)
    target.write("\n")
    target.close()
