for s in `cat samples | grep -v "#" | grep -v "samples"`; do  
    python ${T3COOKER_BASE_DIR}/t3cooker -c $s $1 $2; 
done
