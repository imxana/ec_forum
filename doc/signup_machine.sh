


number=30

name=`rig | head -n 1 | sed 's/ /_/g'`
email=`echo $name | sed 's/_[A-Za-z]*/\@gmail\.com/g'`
psw=`rig | sed -n 3p | grep -E -o '[0-9]*$'`

echo $name $email $psw


sign_up(){
    @curl -d 'u_name='$name'&u_psw='$psw 'http://localhost:5000/sign_up'
}



