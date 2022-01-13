# 234 out of 252 516 alunos are registered in more than one year; 
# we will then select the year based on the rules defined in inscricoes

#create table avaliacao_singlerow_per_discipline_group as
select
	nProcesso,
	agrupamento,
	anoLetivo_c,
	ano_c,
	periodo,
	disciplina_agg,
	# flags if nuclear discipline (portugues or matematica)
	max(nuclear_flag) as nuclear_flag,
	# flags if any of the disciplines in discipline group as an adapted curriculum
	max(adapted_curric_flag) as adapted_curric_flag,
	# average grade for the discipline group
	avg(class_c) as average_grade,
	sum(negative_class)/count(*) as negative_class_ratio,
	count(*) as disciplines_in_group
	from
	(
		select
			nProcesso,
			agrupamento,
			left(anoLetivo, 4) as anoLetivo_c,
			ciclo,
			right(ano, 1) as ano_c,
			periodo,
			disciplina_agg,
			case
				when disciplina_agg = 'portugues' or disciplina_agg = 'matematica' then 1
				else 0
			end as nuclear_flag,
			case
				when class_c < 3 then 1
				else 0
			end as negative_class,
			adapted_curric_flag,
			class_c
		from (
		# select only 2nd and 3rd cycle
		select
				nProcesso,
				agrupamento,
				anoLetivo,
				ciclo,
				ano,
				periodo,
				case
					# For some school groups M is Music, for others is Mathematics; as such M needs to be further classified
					when disciplina = 'M' and agrupamento in ('A2', 'A45') then 'MATEM'
					when disciplina = 'M' and agrupamento in ('A7', 'A10', 'A41', 'A42', 'A43', 'A44',  'A46', 'A47', 'A48', 'A49', 'A52') then 'E.MUS'
					# For some school groups LP is Lingua Portuguesa, for others is Leitura de Partituras; as such L.P. needs to be further classified
					when disciplina = 'LP' and agrupamento = 'A4' then 'Leitura Partituras'
					else disciplina
				end as disciplina,
				# keep the highest grade obtained by the student
				max(class) as class_c
			from atb2.avaliacao a
			where ciclo in ('2C', '3C') and right(ano, 1) in ('5', '6', '7', '8', '9') and class in ('1', '2', '3', '4', '5')
			group by
				nProcesso,
				agrupamento,
				anoLetivo,
				ciclo,
				ano,
				periodo,
				disciplina
				) filter_ciclo
		left join correspondencia_disciplina cd
		on filter_ciclo.disciplina = cd.disciplina_raw
		) aggregate_discipline_group
	group by
		nProcesso,
		agrupamento,
		anoLetivo_c,
		ano_c,
		periodo,
		disciplina_agg
