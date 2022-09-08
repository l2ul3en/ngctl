_get_frec(){
#Devuelve la cantidad de repeticiones de la cadena recibida por parametro
    local c i
    c=0
    for ((i=2; i<${#COMP_WORDS[@]}; i++)); do 
        if [[ ${COMP_WORDS[i]} == $1 ]] && [[ ${#COMP_WORDS[i]} -eq ${#1} ]]; then
            c=$(($c+1))
        fi
    done
    echo $c
}
_get_tam(){
#Obtiene la longitud del array sin tomar en cuenta las cadenas vacias
    local c i
    c=0
    for ((i=0; i<${#COMP_WORDS[@]}; i++)); do
        if [[ ${COMP_WORDS[i]} != '' ]]; then
            c=$(($c+1))
        fi
    done
    echo $c
}
_get_posicion(){
#Devuelve la posicion de la cadena edit
    local i=0
    until [[ $i -lt ${#COMP_WORDS[@]} ]] && [[ ${COMP_WORDS[i]} == edit ]]; do
        i=$(($i+1))
    done
    echo $(($i+1))
}
_get_cant_opciones_host(){
#Retorna un array por tipo (booleano, con/sin parametro) de la cantidad de las opciones del modulo host
    local con_parametro=0; local boleano=0; local sin_parametro=0; local i=2
    until [[ $i -ge ${#COMP_WORDS[@]} ]] || [[ ${COMP_WORDS[i]} == edit ]]; do
        case ${COMP_WORDS[i]} in
            --ip|--copy|--rename|-r|-c) con_parametro=$(($con_parametro+1)); i=$(($i+1));;
            --delete|--show|--list|-l|--generate|-g|--groups|-G|--verbose|-v|-d|-s|-h|--help) boleano=$(($boleano+1));;
            '') : ;;
            *) sin_parametro=$(($sin_parametro+1)) ;;
        esac
        i=$(($i+1))
    done
    echo $boleano $con_parametro $sin_parametro
}

_get_cant_opciones_group(){
#Retorna un array por tipo (booleano, con/sin parametro) de la cantidad de las opciones del modulo group
    local con_parametro=0; local boleano=0; local sin_parametro=0; local i=2
    until [[ $i -ge ${#COMP_WORDS[@]} ]] || [[ ${COMP_WORDS[i]} == edit ]]; do
        case ${COMP_WORDS[i]} in
            --copy|--rename|-r|-c) con_parametro=$(($con_parametro+1)); i=$(($i+1));;
            --delete|--show|--list|-l|-d|-s|-h|--help) boleano=$(($boleano+1));;
            '') : ;;
            *) sin_parametro=$(($sin_parametro+1)) ;;
        esac
        i=$(($i+1))
    done
    echo $boleano $con_parametro $sin_parametro
}

_get_cant_opciones_service(){
#Retorna un array por tipo (booleano, con/sin parametro) de la cantidad de las opciones del modulo service
    local con_parametro=0; local boleano=0; local sin_parametro=0; local i=2
    until [[ $i -ge ${#COMP_WORDS[@]} ]] || [[ ${COMP_WORDS[i]} == edit ]]; do
        case ${COMP_WORDS[i]} in
            --host|--copy|--rename|-r|-c) con_parametro=$(($con_parametro+1)); i=$(($i+1));;
            --delete|--show|-d|-s|-h|--help) boleano=$(($boleano+1));;
            '') : ;;
            *) sin_parametro=$(($sin_parametro+1)) ;;
        esac
        i=$(($i+1))
    done
    echo $boleano $con_parametro $sin_parametro
}
_get_cant_opciones_edit(){
#Retorna un array por tipo (booleano, con/sin parametro) de la cantidad de las opciones del submodulo edit
    local con_parametro=0; local boleano=0; local sin_parametro=0; local i
    for ((i=$(_get_posicion); i<${#COMP_WORDS[@]}; i++)); do
        case ${COMP_WORDS[i]} in
            --add-elemento|--modify|--new|--delete-elemento|-a|-m|-n|-x) con_parametro=$(($con_parametro+1)); i=$(($i+1));;
            --delete|--get|-d|-g|-h|--help) boleano=$(($boleano+1));;
            '') : ;;
            *) sin_parametro=$(($sin_parametro+1)) ;;
        esac
    done
    echo $boleano $con_parametro $sin_parametro
}
# Determines the first non-option word of the command line. This
# is usually the command
_sy_get_firstword() {
	local firstword i
	firstword=
	for ((i = 1; i < ${#COMP_WORDS[@]}; ++i)); do
		if [[ ${COMP_WORDS[i]} != -* ]]; then
			firstword=${COMP_WORDS[i]}
			break
		fi
	done
	echo $firstword
}

# Determines the last non-option word of the command line. This
# is usally a sub-command
_sy_get_lastword() {
	local lastword i
	lastword=
	for ((i = 1; i < ${#COMP_WORDS[@]}; ++i)); do
		if [[ ${COMP_WORDS[i]} != -* ]] && [[ -n ${COMP_WORDS[i]} ]] && [[ ${COMP_WORDS[i]} != $cur ]]; then
			lastword=${COMP_WORDS[i]}
		fi
	done
	echo $lastword
}

_get_cant_opciones_command(){
#Retorna un array por tipo (booleano, con/sin parametro) de la cantidad de las opciones del modulo command
    local con_parametro=0; local boleano=0; local sin_parametro=0; local i=2
    until [[ $i -ge ${#COMP_WORDS[@]} ]] || [[ ${COMP_WORDS[i]} == edit ]]; do
        case ${COMP_WORDS[i]} in
            --copy|--rename|-r|-c) con_parametro=$(($con_parametro+1)); i=$(($i+1));;
            --delete|--show|-d|-s|-h|--help) boleano=$(($boleano+1));;
            '') : ;;
            *) sin_parametro=$(($sin_parametro+1)) ;;
        esac
        i=$(($i+1))
    done
    echo $boleano $con_parametro $sin_parametro
}

_get_cant_opciones_contact(){
#Retorna un array por tipo (booleano, con/sin parametro) de la cantidad de las opciones del modulo contact
    local con_parametro=0; local boleano=0; local sin_parametro=0; local i=2
    until [[ $i -ge ${#COMP_WORDS[@]} ]] || [[ ${COMP_WORDS[i]} == edit ]]; do
        case ${COMP_WORDS[i]} in
            --copy|--rename|-r|-c) con_parametro=$(($con_parametro+1)); i=$(($i+1));;
            --delete|--show|-d|-s|-h|--help|-G|--groups) boleano=$(($boleano+1));;
            '') : ;;
            *) sin_parametro=$(($sin_parametro+1)) ;;
        esac
        i=$(($i+1))
    done
    echo $boleano $con_parametro $sin_parametro
}

_get_cant_opciones_contactgroup(){
#Retorna un array por tipo (booleano, con/sin parametro) de la cantidad de las opciones del modulo contactgroup
    local con_parametro=0; local boleano=0; local sin_parametro=0; local i=2
    until [[ $i -ge ${#COMP_WORDS[@]} ]] || [[ ${COMP_WORDS[i]} == edit ]]; do
        case ${COMP_WORDS[i]} in
            --copy|--rename|-r|-c) con_parametro=$(($con_parametro+1)); i=$(($i+1));;
            --delete|--show|-d|-s|-h|--help) boleano=$(($boleano+1));;
            '') : ;;
            *) sin_parametro=$(($sin_parametro+1)) ;;
        esac
        i=$(($i+1))
    done
    echo $boleano $con_parametro $sin_parametro
}

_nagiosctl(){
	local cur prev complete_options complete_words tam firstword lastword
	COMPREPLY=()
	cur=${COMP_WORDS[COMP_CWORD]}
	prev=${COMP_WORDS[COMP_CWORD-1]}
	firstword=$(_sy_get_firstword)
	lastword=$(_sy_get_lastword)
	tam=${#COMP_WORDS[@]}

	GLOBAL_MODULE="\
		search\
		group\
		service\
		host\
		export\
		command\
		contact\
		contactgroup"

	GLOBAL_OPTIONS="-h --help"

	SEARCH_OPTIONS="\
		-h --help\
		-a --atributo\
		-r --regexp\
		-f --force-name"

	GROUP_OPTIONS="\
		-h --help\
		-c --copy\
		-d --delete\
		-l --list\
		-r --rename\
		-s --show"

	SERVICE_OPTIONS="\
		-h --help\
		-c --copy\
		-d --delete\
		-r --rename\
		-s --show\
		--host"

	HOST_OPTIONS="\
		-h --help\
		-l --list\
		-c --copy\
		-d --delete\
		-g --generate\
		-G --groups\
		-r --rename\
		-s --show\
		--ip\
		-v --verbose"

	EDIT_OPTIONS="\
		-h --help\
		-a --add-elemento\
		-d --delete\
		-g --get\
		-m --modify\
		-n --new\
		-x --delete-elemento"

	EXPORT_OPTIONS="\
		-h --help\
		-c --columns\
		-I --Input\
		-O --Output\
		-d --delimiter"

	COMMAND_OPTIONS="\
		-h --help\
		-c --copy\
		-d --delete\
		-r --rename\
		-s --show"

	CONTACT_OPTIONS="\
		-h --help\
		-c --copy\
		-d --delete\
		-G --groups\
		-r --rename\
		-s --show"

	CONTACTGROUP_OPTIONS=$COMMAND_OPTIONS

	OBJETOS='alarma host grupo command contact contactgroup'

	#Un-comment this for debug purposes:
	#echo -e "prev = $prev, cur = $cur, firstword = $firstword, lastword = $lastword, len = $tam" >> /home/manfred/compl.log

	case $firstword in
		
		export)
			if [[ ($prev == export) && ($tam -le 3) ]]; then
				COMPREPLY=( $(compgen -W "$OBJETOS" -- $cur) ); return 0
			elif [[ $tam -ge 3 ]]; then
				complete_options=$EXPORT_OPTIONS
			fi	
			;;

		search)
		
			if [[ ($prev == search) && ($tam -le 3) ]]; then
				COMPREPLY=( $(compgen -W "$OBJETOS" -- $cur) ); return 0
			elif [[ ($tam -ge 3) && ($tam -le 8) ]]; then
				complete_options=$SEARCH_OPTIONS
			fi
			;;

		group)

			local exist_edit exist_host exist_grupo exist_edit_name cant_opc_grupo cant_opc_edit param_total e_bool e_con_para e_sin_para tam_real 
			exist_edit=$(_get_frec 'edit')
			lista=($(_get_cant_opciones_group))
#			echo "group: ${lista[@]}" >> ~/compl.log
			booleano=${lista[0]}
			con_parametro=${lista[1]}
			sin_parametro=${lista[2]}
			tam_real=$(_get_tam)
			exist_grupo=$sin_parametro
			cant_opc_grupo=$(($booleano+$con_parametro))
			param_total=$(( $booleano+$sin_parametro+2+($con_parametro*2) ))
#			echo "par=$con_parametro, bol=$booleano, arg-posic=$sin_parametro, tam_real=$tam_real, total=$param_total" >> ~/compl.log
			if [[ $exist_edit -eq 1 ]]; then
				arr=($(_get_cant_opciones_edit))
#				echo "edit: ${arr[@]}" >> ~/compl.log
				e_bool=${arr[0]}
				e_con_para=${arr[1]}
				e_sin_para=${arr[2]}
				tam_real=$(_get_tam)
				exist_edit_name=$e_sin_para
				cant_opc_edit=$(($e_bool+$e_con_para))
				param_total=$(( $param_total+1+$e_bool+$e_sin_para+($e_con_para*2) ))
#				echo "edit_param=$cant_opc_edit, atributo-name=$exist_edit_name, tam_real=$tam_real, total=$param_total" >> ~/compl.log
			fi
			if [[ ($exist_edit -eq 0 ) && ($prev != group ) && (($cant_opc_grupo -le 1) && ($exist_grupo -eq 1) && ($param_total -eq $tam_real)) && ($tam -eq 4) && ($cur != -* ) ]]; then
				COMPREPLY=( $(compgen -W "edit" -- $cur) ); return 0
			elif [[ ($exist_edit -eq 0 ) && ($tam -lt 5) ]]; then
				complete_options=$GROUP_OPTIONS
			elif [[ ($exist_edit -eq 1) && (($tam -ge 5) && ($tam -le 6)) && ($prev != -* ) && (($cant_opc_edit -le 1) && ($exist_edit_name -le 2) && ($param_total -eq $tam_real)) ]]; then
				complete_options=$EDIT_OPTIONS
			else
				return 0
			fi

			;;
		service)
			local exist_edit exist_host exist_alarma exist_edit_name cant_opc_serv cant_opc_edit param_total 
			exist_edit=$(_get_frec 'edit')
			exist_host=$(_get_frec '--host')
#			echo "edit=$exist_edit, host=$exist_host" >> ~/compl.log

			lista=($(_get_cant_opciones_service))
#			echo "service: ${lista[@]}" >> ~/compl.log
			booleano=${lista[0]}
			con_parametro=${lista[1]}
			sin_parametro=${lista[2]}
			tam_real=$(_get_tam)
			exist_alarma=$sin_parametro
			cant_opc_serv=$(($booleano+$con_parametro))
			param_total=$(( $booleano+$sin_parametro+2+($con_parametro*2) ))
#			echo "par=$con_parametro, bol=$booleano, atr=$sin_parametro, tam_real=$tam_real, total=$param_total" >> ~/compl.log

			if [[ $exist_edit -eq 1 ]]; then
				arr=($(_get_cant_opciones_edit))
#				echo "edit: ${arr[@]}" >> ~/compl.log
				e_bool=${arr[0]}
				e_con_para=${arr[1]}
				e_sin_para=${arr[2]}
				tam_real=$(_get_tam)
				exist_edit_name=$e_sin_para
				cant_opc_edit=$(($e_bool+$e_con_para))
				param_total=$(( $param_total+1+$e_bool+$e_sin_para+($e_con_para*2) ))
#				echo "edit_param=$cant_opc_edit, atributo-name=$exist_edit_name, tam_real=$tam_real, total=$param_total" >> ~/compl.log
			fi

			if [[ ($exist_edit -eq 0) && ($prev != service ) && (($cant_opc_serv -eq 0) || (($exist_host -eq 1) && ($cant_opc_serv -eq 1)) && ($exist_alarma -eq 1) && ($param_total -eq $tam_real)) && (($tam -ge 4) && ($tam -lt 7)) && ($cur != -* ) ]]; then

				COMPREPLY=( $(compgen -W "edit" -- $cur) ); return 0

			elif [[ ($exist_edit -eq 0) && (($tam -ge 3) && ($tam -le 6)) ]]; then

				complete_options=$SERVICE_OPTIONS

			elif [[ ((($exist_edit -eq 1) && ($exist_host -eq 1)) && (($tam -ge 7) && ($tam -le 10)) && ($prev != -* ) && (($cant_opc_edit -le 1) && ($exist_edit_name -le 2) && ($param_total -eq $tam_real))) || ( (($exist_edit -eq 1) && ($exist_host -eq 0)) && (($tam -ge 5) && ($tam -le 7 )) && ($prev != -* ) && (($cant_opc_edit -le 1) && ($exist_edit_name -le 2) && ($param_total -eq $tam_real))) ]]; then

				complete_options=$EDIT_OPTIONS
			else
				return 0
			fi

			;;
		host)
			local exist_edit exist_ip exist_host exist_edit_name cant_opc_host cant_opc_edit param_total 
			exist_edit=$(_get_frec 'edit')
			exist_ip=$(_get_frec '--ip')
#			echo "edit=$exist_edit, ip=$exist_ip" >> ~/compl.log

			lista=($(_get_cant_opciones_host))
#			echo "host: ${lista[@]}" >> ~/compl.log
			booleano=${lista[0]}
			con_parametro=${lista[1]}
			sin_parametro=${lista[2]}
			tam_real=$(_get_tam)
			exist_host=$sin_parametro
			cant_opc_host=$(($booleano+$con_parametro))
			param_total=$(( $booleano+$sin_parametro+2+($con_parametro*2) ))
#			echo "par=$con_parametro, bol=$booleano, atr=$sin_parametro, tam_real=$tam_real, total=$param_total" >> ~/compl.log

			if [[ $exist_edit -eq 1 ]]; then
				arr=($(_get_cant_opciones_edit))
#				echo "edit: ${arr[@]}" >> ~/compl.log
				e_bool=${arr[0]}
				e_con_para=${arr[1]}
				e_sin_para=${arr[2]}
				tam_real=$(_get_tam)
				exist_edit_name=$e_sin_para
				cant_opc_edit=$(($e_bool+$e_con_para))
				param_total=$(( $param_total+1+$e_bool+$e_sin_para+($e_con_para*2) ))
#				echo "edit_param=$cant_opc_edit, atributo-name=$exist_edit_name, tam_real=$tam_real, total=$param_total" >> ~/compl.log
			fi

			if [[ ($exist_edit -eq 0) && ($prev != host ) && (($cant_opc_host -eq 0) && ($exist_host -eq 1) && ($param_total -eq $tam_real)) && ($tam -ge 4) && ($cur != -* ) ]]; then

				COMPREPLY=( $(compgen -W "edit" -- $cur) ); return 0

			elif [[ ($exist_edit -eq 0) && (($tam -ge 3) && ($tam -le 6)) ]]; then

				complete_options=$HOST_OPTIONS

			elif [[ ((($exist_edit -eq 1) && ($exist_ip -eq 1)) && (($tam -ge 7) && ($tam -le 10)) && ($prev != -* ) && (($cant_opc_edit -le 1) && ($exist_edit_name -le 2) && ($param_total -eq $tam_real))) || ( (($exist_edit -eq 1) && ($exist_ip -eq 0)) && (($tam -ge 5) && ($tam -le 7 )) && ($prev != -* ) && (($cant_opc_edit -le 1) && ($exist_edit_name -le 2) && ($param_total -eq $tam_real))) ]]; then

				complete_options=$EDIT_OPTIONS
			else
				return 0
			fi
			;;
		command)

			local exist_cmd cant_opc_cmd
			local exist_edit exist_edit_name cant_opc_edit param_total e_bool e_con_para e_sin_para tam_real lista arr
			exist_edit=$(_get_frec 'edit')
			lista=($(_get_cant_opciones_command))
#			echo "group: ${lista[@]}" >> ~/compl.log
			booleano=${lista[0]}
			con_parametro=${lista[1]}
			sin_parametro=${lista[2]}
			tam_real=$(_get_tam)
			exist_cmd=$sin_parametro
			cant_opc_cmd=$(($booleano+$con_parametro))
			param_total=$(( $booleano+$sin_parametro+2+($con_parametro*2) ))
#			echo "par=$con_parametro, bol=$booleano, arg-posic=$sin_parametro, tam_real=$tam_real, total=$param_total" >> ~/compl.log
			if [[ $exist_edit -eq 1 ]]; then
				arr=($(_get_cant_opciones_edit))
#				echo "edit: ${arr[@]}" >> ~/compl.log
				e_bool=${arr[0]}
				e_con_para=${arr[1]}
				e_sin_para=${arr[2]}
				tam_real=$(_get_tam)
				exist_edit_name=$e_sin_para
				cant_opc_edit=$(($e_bool+$e_con_para))
				param_total=$(( $param_total+1+$e_bool+$e_sin_para+($e_con_para*2) ))
#				echo "edit_param=$cant_opc_edit, atributo-name=$exist_edit_name, tam_real=$tam_real, total=$param_total" >> ~/compl.log
			fi
			if [[ ($exist_edit -eq 0 ) && ($prev != command ) && (($cant_opc_cmd -le 1) && ($exist_cmd -eq 1) && ($param_total -eq $tam_real)) && ($tam -eq 4) && ($cur != -* ) ]]; then
				COMPREPLY=( $(compgen -W "edit" -- $cur) ); return 0
			elif [[ ($exist_edit -eq 0 ) && ($tam -lt 5) ]]; then
				complete_options=$COMMAND_OPTIONS
			elif [[ ($exist_edit -eq 1) && (($tam -ge 5) && ($tam -le 6)) && ($prev != -* ) && (($cant_opc_edit -le 1) && ($exist_edit_name -le 2) && ($param_total -eq $tam_real)) ]]; then
				complete_options=$EDIT_OPTIONS
			else
				return 0
			fi
			;;

		contact)
			local exist_cnt cant_opc_cnt
			local exist_edit exist_edit_name cant_opc_edit param_total e_bool e_con_para e_sin_para tam_real lista arr
			exist_edit=$(_get_frec 'edit')
			lista=($(_get_cant_opciones_contact))
#			echo "group: ${lista[@]}" >> ~/compl.log
			booleano=${lista[0]}
			con_parametro=${lista[1]}
			sin_parametro=${lista[2]}
			tam_real=$(_get_tam)
			exist_cnt=$sin_parametro
			cant_opc_cnt=$(($booleano+$con_parametro))
			param_total=$(( $booleano+$sin_parametro+2+($con_parametro*2) ))
#			echo "par=$con_parametro, bol=$booleano, arg-posic=$sin_parametro, tam_real=$tam_real, total=$param_total" >> ~/compl.log
			if [[ $exist_edit -eq 1 ]]; then
				arr=($(_get_cant_opciones_edit))
#				echo "edit: ${arr[@]}" >> ~/compl.log
				e_bool=${arr[0]}
				e_con_para=${arr[1]}
				e_sin_para=${arr[2]}
				tam_real=$(_get_tam)
				exist_edit_name=$e_sin_para
				cant_opc_edit=$(($e_bool+$e_con_para))
				param_total=$(( $param_total+1+$e_bool+$e_sin_para+($e_con_para*2) ))
#				echo "edit_param=$cant_opc_edit, atributo-name=$exist_edit_name, tam_real=$tam_real, total=$param_total" >> ~/compl.log
			fi
			if [[ ($exist_edit -eq 0 ) && ($prev != contact ) && (($cant_opc_cnt -le 1) && ($exist_cnt -eq 1) && ($param_total -eq $tam_real)) && ($tam -eq 4) && ($cur != -* ) ]]; then
				COMPREPLY=( $(compgen -W "edit" -- $cur) ); return 0
			elif [[ ($exist_edit -eq 0 ) && ($tam -lt 5) ]]; then
				complete_options=$CONTACT_OPTIONS
			elif [[ ($exist_edit -eq 1) && (($tam -ge 5) && ($tam -le 6)) && ($prev != -* ) && (($cant_opc_edit -le 1) && ($exist_edit_name -le 2) && ($param_total -eq $tam_real)) ]]; then
				complete_options=$EDIT_OPTIONS
			else
				return 0
			fi
			;;

		contactgroup)
			local exist_cgr cant_opc_cgr
			local exist_edit exist_edit_name cant_opc_edit param_total e_bool e_con_para e_sin_para tam_real lista arr
			exist_edit=$(_get_frec 'edit')
			lista=($(_get_cant_opciones_contactgroup))
#			echo "group: ${lista[@]}" >> ~/compl.log
			booleano=${lista[0]}
			con_parametro=${lista[1]}
			sin_parametro=${lista[2]}
			tam_real=$(_get_tam)
			exist_cgr=$sin_parametro
			cant_opc_cgr=$(($booleano+$con_parametro))
			param_total=$(( $booleano+$sin_parametro+2+($con_parametro*2) ))
#			echo "par=$con_parametro, bol=$booleano, arg-posic=$sin_parametro, tam_real=$tam_real, total=$param_total" >> ~/compl.log
			if [[ $exist_edit -eq 1 ]]; then
				arr=($(_get_cant_opciones_edit))
#				echo "edit: ${arr[@]}" >> ~/compl.log
				e_bool=${arr[0]}
				e_con_para=${arr[1]}
				e_sin_para=${arr[2]}
				tam_real=$(_get_tam)
				exist_edit_name=$e_sin_para
				cant_opc_edit=$(($e_bool+$e_con_para))
				param_total=$(( $param_total+1+$e_bool+$e_sin_para+($e_con_para*2) ))
#				echo "edit_param=$cant_opc_edit, atributo-name=$exist_edit_name, tam_real=$tam_real, total=$param_total" >> ~/compl.log
			fi
			if [[ ($exist_edit -eq 0 ) && ($prev != contactgroup ) && (($cant_opc_cgr -le 1) && ($exist_cgr -eq 1) && ($param_total -eq $tam_real)) && ($tam -eq 4) && ($cur != -* ) ]]; then
				COMPREPLY=( $(compgen -W "edit" -- $cur) ); return 0
			elif [[ ($exist_edit -eq 0 ) && ($tam -lt 5) ]]; then
				complete_options=$CONTACTGROUP_OPTIONS
			elif [[ ($exist_edit -eq 1) && (($tam -ge 5) && ($tam -le 6)) && ($prev != -* ) && (($cant_opc_edit -le 1) && ($exist_edit_name -le 2) && ($param_total -eq $tam_real)) ]]; then
				complete_options=$EDIT_OPTIONS
			else
				return 0
			fi
			;;

		*)
			if [[ $tam -eq 2 ]]; then	
				complete_words="$GLOBAL_MODULE"
				complete_options="$GLOBAL_OPTIONS"
			else
				return 0
			fi
			;;
	esac
	
# Either display words or options, depending on the user input
	if [[ $cur == -* ]]; then
		COMPREPLY=( $( compgen -W "$complete_options" -- $cur ))
	elif [[ $cur != '' ]] || [[ $prev == 'nagiosctl' ]]; then
		COMPREPLY=( $( compgen -W "$complete_words" -- $cur ))
	fi
					 
	return 0
}
#complete -F _nagiosctl -o bashdefault -o default nagiosctl
complete -F _nagiosctl nagiosctl
