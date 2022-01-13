#create table atb2.alunos_inscricoes_singlerow as 
select 
	alunos.nProcesso, alunos.agrupamento, alunos.anoLetivo, 
	ano,
	turma,
	escalao,
	nee,
	`dataNascimento a`,
	genero,
	nacionalidade,
	linguaMaterna,
	anoEscMae,
	`concelho a`, 
	distrito,
	transferencia,
	abandono,
	rFinal,
	estado
from 
	atb2.alunos_singlerow alunos
inner join 
	atb2.inscricoes_singlerow inscricoes
on 
	alunos.nProcesso = inscricoes.nProcesso and 
	alunos.agrupamento = inscricoes.agrupamento and 
	# join with the first 4 digits to avoid differences in date format and extra characters
	LEFT(alunos.anoLetivo, 4) = LEFT(inscricoes.anoLetivo, 4)
