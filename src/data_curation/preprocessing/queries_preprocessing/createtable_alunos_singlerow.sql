# Starting from alunos table shared by the partner
# this query creates a table with one entry 
# per student, school group and school year

# data entry issues created duplicated entries
# when NEE or socio-economic status were updated
# if the student was flagged for NEE at any point in the year
# we keep that information
# and we keep the lowest socio-economic value they had in the year
# (corresponding to higher level of economic help)


#create table atb2.alunos_singlerow as
select
	nProcesso,
	anoLetivo,
	agrupamento,
	min(escalao_c) as escalao,
	max(nee_c) as nee,
	`dataNascimento a`,
	genero,
	nacionalidade,
	linguaMaterna,
	anoEscMae,
	`concelho a`,
	distrito
	from
	(
		select distinct
		nProcesso,
		anoLetivo,
		agrupamento,
		case
			when nee = '' then '0'
			when nee = '0' then '0'
			when nee = 'FALSE' then '0'
			when nee = 'TRUE' then '1'
			when nee = '1' then '1'
			else '0'
		end as nee_c,
		case
			when trim(escalao) = 'A' then '1'
			when trim(escalao) = 'B' then '2'
			when trim(escalao) = 'C' then '3'
			when escalao = '1' then '1'
			when escalao = '2' then '2'
			else '3'
		end as escalao_c,
		`dataNascimento a`,
		genero,
		nacionalidade,
		linguaMaterna,
		anoEscMae,
		`concelho a`,
		distrito
		from atb2.alunos a
	) a
group by
	nProcesso,
	anoLetivo,
	agrupamento,
	`dataNascimento a`,
	genero,
	nacionalidade,
	linguaMaterna,
	anoEscMae,
	`concelho a`,
	distrito



