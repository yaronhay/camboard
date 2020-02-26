#!/bin/bash
address=$1
subject=$2
content=$3
file_path=$4

echo "tell application \"Mail\"
	activate

	set MyEmail to make new outgoing message with properties {visible:true, subject:\"$subject\", content:\"$content\"}
	tell MyEmail
		make new to recipient at end of to recipients with properties {address:\"$address\"}
		make new attachment with properties {file name:((\"$file_path\" as POSIX file) as alias)}
		delay 1
		send
	end tell
end tell" | osascript