#create table atb2.inscricoes_singlerow as 
select 
	nProcesso,
	ano_c as ano, 
	turma_c as turma,
	dEntrada_c as dEntrada,
	transferencia_c as transferencia,
	abandono_c as abandono,
	rFinal_c as rFinal,
	estado_c as estado,
	anoLetivo_c as anoLetivo,
	agrupamento
from (
	select  
		*,
		# priority rules to define the line to keep: 
			# a) most recent date of entry, 
			# b) if there is any line where the student was approved or failed the year, 
			# c) if there is any line indicating the student is registered (estado)
			# c) if there is any line indicating if the student dropped out 
			# d) the minimum school year
		ROW_NUMBER() OVER (PARTITION BY nProcesso, agrupamento, anoLetivo_c ORDER BY dEntrada_c desc, rFinal_c desc, estado_c desc, abandono_c desc, ano_c asc) as row_num
	FROM
	(
			select 
				nProcesso,
				ano_c, 
				dEntrada_c,
				# store info if the student was transfered in the current school year
				max(transferencia_c) as transferencia_c,
				GROUP_CONCAT(turma SEPARATOR ', ') as turma_c,
				abandono_c,
				rFinal_c,
				estado_c,
				anoLetivo_c,
				agrupamento
			from 
			(
			select distinct 
				nProcesso,
				right(ano, 1) as ano_c,
				turma,
				case 
					when left(dEntrada, 3) = "200" then STR_TO_DATE(REPLACE(LEFT(dEntrada, 10), '-', '/'),'%Y/%m/%d') 
					when left(dEntrada, 3) = "201" then STR_TO_DATE(REPLACE(LEFT(dEntrada, 10), '-', '/'),'%Y/%m/%d') 
					when left(dEntrada, 3) = "202" then STR_TO_DATE(REPLACE(LEFT(dEntrada, 10), '-', '/'),'%Y/%m/%d') 
					else STR_TO_DATE(REPLACE(LEFT(dEntrada, 10), '-', '/'),'%d/%m/%Y') 
				end as dEntrada_c,
				case 
					when transferencia = 'false' then '0'
					when transferencia = 'true' then '1'
					else transferencia
				end as transferencia_c,
				case 
					when abandono = 'false' then '0'
					when abandono = 'true' then '1'
					else abandono 
				end as abandono_c,
				case 
					when rFinal = 'Transitou' then '2'
					when rFinal = 'Aprovado' then '2'
					when rFinal = 'Admitido a Exame' then '2'
					when rFinal like 'Admitido a Est%gio' then '2'
					when rFinal = 'Prosseguiu' then '2'
					when rFinal = 'Mudou de Ano' then '2'
					when rFinal like 'N%o Transitou' then '1'
					when rFinal like 'N%o Aprovado' then '1'
					when rFinal like '% por faltas' then '1'
					when rFinal like 'Anulou matr%cula' then '1'
					when rFinal like 'N%o prosseguiu' then '1'
					when rFinal like 'Em Proc. Avalia%o' then '0'
					when rFinal like 'Em processo de avalia%o' then '0'
					when rFinal = 'Pendente' then '0'
					when rFinal = 'NULL' then '0'
					when rFinal like 'Mudou Situa%o' then '0'
					when rFinal = 'Matriculado' then '0'
					when rFinal = '' then '0'
				end as rFinal_c,
				case 
					when estado = 'false' then '0'
					when estado = 'true' then '1'
					else estado
				end as estado_c,
				# some school groups have information about anoLetivo in another column 
				case 
					when anoLetivo is null then `anosescolares.descricao`
					else anoLetivo
				end as anoLetivo_c,
				agrupamento
			from 
			atb2.inscricoes
			where right(ano, 1) >= 5
			) recode_vars
		group by 
			nProcesso,
			ano_c, 
			dEntrada_c,
			abandono_c,
			rFinal_c,
			estado_c,
			anoLetivo_c,
			agrupamento
		) get_max_transferencia
	) attribute_row_number 
	# select first line (according to the rules defined above) per student, year, school group
	where row_num = 1
