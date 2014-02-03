#!/bin/tcsh -f

foreach x ( `rfdir $1 | grep root | awk '{print $NF}' | sort -g -t _ -k 2 | awk -F _ '{print $2}' | uniq -d` )

#Print all duplicates
if ( 0 ) then
    foreach y ( `rfdir $1 | grep hzzPatSkim_${x}_ | awk '{print $NF}' ` )
	echo 1/$y
    end
    echo "\n"

else 
#Print files to be removed
    set keep=1
    foreach y ( `rfdir $1 | grep hzzPatSkim_${x}_ | awk '{print $NF}' | sort -r` )
	if ( $keep == 1 ) then
	    set keep=0
	else
	    echo rfrm $1/$y
	endif
    end
endif
end




