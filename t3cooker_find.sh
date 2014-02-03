rm special_t3cooker_jobs.sh; 
for s in `cat samples | grep -v "#"`; do 
	t3cooker -c $s --status > status_tmp; 
	jobs=`grep -A10 "Job Summary" status_tmp | grep "$1" | grep ":" | awk -F":" '{print $2}'`; 
	echo "t3cooker -c "$s "\$1 "$jobs >> special_t3cooker_jobs.sh; 
done
