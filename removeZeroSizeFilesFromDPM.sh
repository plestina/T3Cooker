#!/bin/bash

# dirs='
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/ZZTo2e2mu
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/ZZTo2e2tau
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/ZZTo2mu2tau
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/ZZTo4e
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/ZZTo4mu
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/ZZTo4tau
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/ggZZ2l2l
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/ggZZ4l
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/H115
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/H120
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/H130
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/H140
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/H160
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/H200
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/H300
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/H350
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/H400
# 
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/H120_looseZ2
# 
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/TTTo2L2Nu2B
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/WZTo3LNuv2
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/ggZZ2l2l
# 
# 
# 
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/DYJetsToLLTuneZ2M10To50
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/DYJetsToLLTuneZ2M50
# 
# 
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/zz2e2tau_powheg
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/zz2e2m_powheg
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/zz2mu2tau_powheg
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/zz4e_powheg
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/zz4tau_powheg
# 
# 
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/16Jan2012_DoubleEle
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/16Jan2012_DoubleEle2011B
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/16Jan2012_DoubleMu
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/16Jan2012_DoubleMu2011B
# 
# 
# '

# 
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/zz2e2tau_powheg
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/zz2e2m_powheg
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/zz2mu2tau_powheg
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/zz4e_powheg
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/zz4tau_powheg
# 
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/CMG/V5_2_0/zz2e2tau_powheg
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/CMG/V5_2_0/zz2e2m_powheg
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/CMG/V5_2_0/zz2mu2tau_powheg
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/CMG/V5_2_0/zz4e_powheg
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/CMG/V5_2_0/zz4mu_powheg
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/CMG/V5_2_0/zz4tau_powheg


# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/16Jan2012_DoubleEle
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/16Jan2012_DoubleEle2011B
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/16Jan2012_DoubleMu
# /dpm/in2p3.fr/home/cms/trivcat/store/user/roko/PATCMGApr23/16Jan2012_DoubleMu2011B


dirs='


/dpm/in2p3.fr/home/cms/trivcat/store/user/roko/CMG/V5_2_0/zz2e2tau_powheg
/dpm/in2p3.fr/home/cms/trivcat/store/user/roko/CMG/V5_2_0/zz2e2m_powheg
/dpm/in2p3.fr/home/cms/trivcat/store/user/roko/CMG/V5_2_0/zz2mu2tau_powheg
/dpm/in2p3.fr/home/cms/trivcat/store/user/roko/CMG/V5_2_0/zz4e_powheg
/dpm/in2p3.fr/home/cms/trivcat/store/user/roko/CMG/V5_2_0/zz4mu_powheg
/dpm/in2p3.fr/home/cms/trivcat/store/user/roko/CMG/V5_2_0/zz4tau_powheg

'


for dir in $dirs; do 
    echo $dir
    rfdir $dir > rfdir.tmp
#     for line in `rfdir $dir | grep "pat" | awk '{print $5" "$9}'`; do
#       for line in `rfdir $dir | grep "pat"`; do
      for line in `cat rfdir.tmp | awk '{print $5","$9}'`; do
      
      #       size=`echo $line | awk -F 'hzzP' '{print $1}'`; 
      #       name=`echo $line | awk -F 'hzzP' '{print "hzzP"$2}'`;
      #       size=`echo $line | awk -F 'pat' '{print $1}'`; 
      #       name=`echo $line | awk -F 'pat' '{print "pat"$2}'`;
# 	  echo $line
	  size=`echo ${line} | awk -F ',' '{print $1}'`; 
	  name=`echo ${line} | awk -F ',' '{print $2}'`;

      #       size=`echo -ne $line | awk '{print $1}'`; 

      #       name=`echo -ne $line | awk '{print $2}'`;    
# 	  echo $size
# 	  echo $name; 



	  if [ ${size} == 0 ]; then 
#       #         echo $size $name; 
	    echo "rfrm "$dir/$name
# 	#     rfrm $dir/$name
	  fi; 
    done
done

# 
# 
# dir=$1
# # echo "Removing 0 size files from "$dir
# 
# for line in `rfdir $dir | awk '{print $5 $9}'`; do 
#   size=`echo $line | awk -F 'hzzP' '{print $1}'`; 
#   name=`echo $line | awk -F 'hzzP' '{print "hzzP"$2}'`;  
#   if [ $size == 0 ]; then 
# #     echo $size $name; 
#     echo "rfrm "$dir/$name
# #     rfrm $dir/$name
#   fi; 
# done
