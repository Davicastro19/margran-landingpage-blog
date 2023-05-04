import os,time,logging
from Controller.controlCatalog import MsgTo
import warnings
warnings.simplefilter("ignore")
warnings.filterwarnings("ignore")
logger = logging.getLogger()
logger.disabled = True
def mpfpl(mpf,width_config,max,min,s,arqname,data,stickCandle,par,timeframe,idd,API_TOKEN):
	mpf.plot(data, type='candle', style=s, 
		mav=(60,20),
		title='Invista - Easy - '+str(par)+' - M'+str(timeframe),
		figsize=(16, 8), scale_padding={'left': 0, 'top': 4, 'right': 0, 'bottom': 0},
		xrotation=52,
		update_width_config=width_config, tight_layout=True,
		hlines=dict(hlines=[max,min,stickCandle[-1]['close']],colors=['g','r','b'],linestyle='-.'),
		savefig=arqname)
	try:
		MsgTo.upload_file(arqname,idd,API_TOKEN)
		time.sleep(3)
		os.remove(arqname)
	except:
		warnings.simplefilter("ignore")
		warnings.filterwarnings("ignore")
		pass