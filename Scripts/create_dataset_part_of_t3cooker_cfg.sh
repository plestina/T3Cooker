for s in `sort samples_V5_START52_V9.list | grep AODSIM`; do 
    sect=`echo $s | awk -F"/" '{print $2}'`; 
    echo "[$sect]"; 
    echo "dataset = $s"; 
    echo "pycfg_params = isMC=1"; 
    echo "";  
done