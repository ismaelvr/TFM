
import ctypes

title = "TFM - BLAKE2"

user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)
screen_size = str(screen_width)+"x"+str(screen_height)

sigma_window_size = "320x220+500+140"
IV_window_size = "160x175+770+470"
rounds_window_size = "685x227+50+440"
gs_window_size = "1140x280+50+720"
internal_state_window_size = "180x90+960+520"
blocks_window_size = "400x270+50+120"
teoric_window_size = "800x420+1000+30"


n_rounds = 12
n_gs = 8
n_step = 8

