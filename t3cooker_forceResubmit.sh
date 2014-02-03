#bash t3cooker_find.sh Aborted; 
echo "Cheching for $1 jobs ..."
bash t3cooker_find.sh $1;
bash special_t3cooker_jobs.sh --kill &> /dev/null; 
bash special_t3cooker_jobs.sh --status &> /dev/null; 
bash special_t3cooker_jobs.sh --submit
