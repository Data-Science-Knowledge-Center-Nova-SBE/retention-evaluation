# create table atb2.avaliacao_singlerow as 
select 
	nProcesso,
	agrupamento,
	anoLetivo_c, 
	ano_c,
	adapted_curric_flag,
	case 
		when negative_class_ratio_1P is null and negative_class_ratio_1S is not null then negative_class_ratio_1S
		else negative_class_ratio_1P
	end as negative_class_ratio_1P,
	case 
		when negative_class_ratio_nuclear_1P is null and negative_class_ratio_nuclear_1S is not null then negative_class_ratio_nuclear_1S
		else negative_class_ratio_nuclear_1P
	end as negative_class_ratio_nuclear_1P,
	case 
		when negative_class_ratio_not_nuclear_1P is null and negative_class_ratio_not_nuclear_1S is not null then negative_class_ratio_not_nuclear_1S
		else negative_class_ratio_not_nuclear_1P
	end as negative_class_ratio_not_nuclear_1P,
	case 
		when negative_class_ratio_2P is null and negative_class_ratio_1S is not null then negative_class_ratio_1S
		else negative_class_ratio_2P
	end as negative_class_ratio_2P,
	case 
		when negative_class_ratio_nuclear_2P is null and negative_class_ratio_nuclear_1S is not null then negative_class_ratio_nuclear_1S
		else negative_class_ratio_nuclear_2P
	end as negative_class_ratio_nuclear_2P,
	case 
		when negative_class_ratio_not_nuclear_2P is null and negative_class_ratio_not_nuclear_1S is not null then negative_class_ratio_not_nuclear_1S
		else negative_class_ratio_not_nuclear_2P
	end as negative_class_ratio_not_nuclear_2P,
	negative_class_ratio_3P,
	negative_class_ratio_nuclear_3P,
	negative_class_ratio_not_nuclear_3P,
	#students in 2C either have ingles or ling_estrang, never both
	case 
		when ano_c < 7 and class1P_ingles is null  and class1P_ling_estrang is not null then class1P_ling_estrang
		when ano_c < 7 and class1P_ingles is null and class1P_ling_estrang is null and class1S_ingles is not null then class1S_ingles
		when ano_c < 7 and class1P_ingles is null and class1P_ling_estrang is null and class1S_ingles is null and class1S_ling_estrang is not null then class1S_ling_estrang
		else class1P_ingles
	end as class1P_ingles_ling_estr,
	case 
		when ano_c < 7 and class2P_ingles is null and class2P_ling_estrang is not null then class2P_ling_estrang
		when ano_c < 7 and class2P_ingles is null and class2P_ling_estrang is null and class1S_ingles is not null then class1S_ingles
		when ano_c < 7 and class2P_ingles is null and class2P_ling_estrang is null and class1S_ingles is null and class1S_ling_estrang is not null then class1S_ling_estrang
		else class2P_ingles
	end as class2P_ingles_ling_estr,
	case 
		when ano_c < 7 and class3P_ingles is null and class3P_ling_estrang is not null then class3P_ling_estrang
		else class3P_ingles
	end as class3P_ingles_ling_estr,
	case
		when class1P_art_tecn is null and class1S_art_tecn is not null then class1S_art_tecn
		else class1P_art_tecn
	end as class1P_art_tecn,
	case
		when class2P_art_tecn is null and class1S_art_tecn is not null then class1S_art_tecn
		else class2P_art_tecn
	end as class2P_art_tecn,
	case
		when class1P_cienc_fis_nat is null and class1S_cienc_fis_nat is not null then class1S_cienc_fis_nat
		else class1P_cienc_fis_nat
	end as class1P_cienc_fis_nat,
	case
		when class2P_cienc_fis_nat is null and class1S_cienc_fis_nat is not null then class1S_cienc_fis_nat
		else class2P_cienc_fis_nat
	end as class2P_cienc_fis_nat,
	case
		when class1P_cienc_soc_huma is null and class1S_cienc_soc_huma is not null then class1S_cienc_soc_huma
		else class1P_cienc_soc_huma
	end as class1P_cienc_soc_huma,
	case
		when class2P_cienc_soc_huma is null and class1S_cienc_soc_huma is not null then class1S_cienc_soc_huma
		else class2P_cienc_soc_huma
	end as class2P_cienc_soc_huma,
	case
		when class1P_ed_fis is null and class1S_ed_fis is not null then class1S_ed_fis
		else class1P_ed_fis
	end as class1P_ed_fis,
	case
		when class2P_ed_fis is null and class1S_ed_fis is not null then class1S_ed_fis
		else class2P_ed_fis
	end as class2P_ed_fis,
	case
		when class1P_ingles is null and class1S_ingles is not null then class1S_ingles
		else class1P_ingles
	end as class1P_ingles,
	case
		when class2P_ingles is null and class1S_ingles is not null then class1S_ingles
		else class2P_ingles
	end as class2P_ingles,
	case
		when class1P_ling_estrang is null and class1S_ling_estrang is not null then class1S_ling_estrang
		else class1P_ling_estrang
	end as class1P_ling_estrang,
	case
		when class2P_ling_estrang is null and class1S_ling_estrang is not null then class1S_ling_estrang
		else class2P_ling_estrang
	end as class2P_ling_estrang,
	case
		when class1P_matematica is null and class1S_matematica is not null then class1S_matematica
		else class1P_matematica
	end as class1P_matematica,
	case
		when class2P_matematica is null and class1S_matematica is not null then class1S_matematica
		else class2P_matematica
	end as class2P_matematica,
	case
		when class1P_portugues is null and class1S_portugues is not null then class1S_portugues
		else class1P_portugues
	end as class1P_portugues,
	case
		when class2P_portugues is null and class1S_portugues is not null then class1S_portugues
		else class2P_portugues
	end as class2P_portugues,
	case
		when class1P_outros is null and class1S_outros is not null then class1S_outros
		else class1P_outros
	end as class1P_outros,
	case
		when class2P_outros is null and class1S_outros is not null then class1S_outros
		else class2P_outros
	end as class2P_outros,
	class3P_art_tecn,
	class3P_cienc_fis_nat,
	class3P_cienc_soc_huma,
	class3P_ed_fis,
	class3P_ingles,
	class3P_ling_estrang,
	class3P_matematica,
	class3P_portugues,
	class3P_outros
from 
(
select 
		nProcesso,
		agrupamento,
		anoLetivo_c, 
		ano_c, 
		# flags if any adapted curriculum variable
		greatest(
			adapted_curric_flag1P_art_tecn,
			adapted_curric_flag1P_cienc_fis_nat,
			adapted_curric_flag1P_cienc_soc_huma,
			adapted_curric_flag1P_ed_fis,
			adapted_curric_flag1P_ingles,
			adapted_curric_flag1P_ling_estrang,
			adapted_curric_flag1P_matematica,
			adapted_curric_flag1P_outros,
			adapted_curric_flag1P_portugues,
			adapted_curric_flag1S_art_tecn,
			adapted_curric_flag1S_cienc_fis_nat,
			adapted_curric_flag1S_cienc_soc_huma,
			adapted_curric_flag1S_ed_fis,
			adapted_curric_flag1S_ingles,
			adapted_curric_flag1S_ling_estrang,
			adapted_curric_flag1S_matematica,
			adapted_curric_flag1S_outros,
			adapted_curric_flag1S_portugues,
			adapted_curric_flag2P_art_tecn,
			adapted_curric_flag2P_cienc_fis_nat,
			adapted_curric_flag2P_cienc_soc_huma,
			adapted_curric_flag2P_ed_fis,
			adapted_curric_flag2P_ingles,
			adapted_curric_flag2P_ling_estrang,
			adapted_curric_flag2P_matematica,
			adapted_curric_flag2P_outros,
			adapted_curric_flag2P_portugues,
			adapted_curric_flag3P_art_tecn,
			adapted_curric_flag3P_cienc_fis_nat,
			adapted_curric_flag3P_cienc_soc_huma,
			adapted_curric_flag3P_ed_fis,
			adapted_curric_flag3P_ingles,
			adapted_curric_flag3P_ling_estrang,
			adapted_curric_flag3P_matematica,
			adapted_curric_flag3P_outros,
			adapted_curric_flag3P_portugues) as adapted_curric_flag,
			# ratio of negative disciplines in 1P
			(IFNULL((negative_class_ratio1P_art_tecn * disciplines_in_group1P_art_tecn), 0) + 
			IFNULL((negative_class_ratio1P_cienc_fis_nat * disciplines_in_group1P_cienc_fis_nat), 0) + 
			IFNULL((negative_class_ratio1P_cienc_soc_huma * disciplines_in_group1P_cienc_soc_huma), 0) + 
			IFNULL((negative_class_ratio1P_ed_fis * disciplines_in_group1P_ed_fis), 0) + 
			IFNULL((negative_class_ratio1P_ingles * disciplines_in_group1P_ingles), 0) + 
			IFNULL((negative_class_ratio1P_ling_estrang * disciplines_in_group1P_ling_estrang), 0) +  
			IFNULL((negative_class_ratio1P_matematica * disciplines_in_group1P_matematica), 0) + 
			IFNULL((negative_class_ratio1P_portugues * disciplines_in_group1P_portugues), 0))/ 
			NULLIF(IFNULL(disciplines_in_group1P_art_tecn, 0) +
			IFNULL(disciplines_in_group1P_cienc_fis_nat, 0) + 
			IFNULL(disciplines_in_group1P_cienc_soc_huma, 0) +
			IFNULL(disciplines_in_group1P_ed_fis, 0) +
			IFNULL(disciplines_in_group1P_ingles, 0) +
			IFNULL(disciplines_in_group1P_ling_estrang, 0) +
			IFNULL(disciplines_in_group1P_matematica, 0) +
			IFNULL(disciplines_in_group1P_portugues, 0), 0) as negative_class_ratio_1P,
			# ratio of negative disciplines in 2P
			(IFNULL((negative_class_ratio2P_art_tecn * disciplines_in_group2P_art_tecn), 0) + 
			IFNULL((negative_class_ratio2P_cienc_fis_nat * disciplines_in_group2P_cienc_fis_nat), 0) + 
			IFNULL((negative_class_ratio2P_cienc_soc_huma * disciplines_in_group2P_cienc_soc_huma), 0) + 
			IFNULL((negative_class_ratio2P_ed_fis * disciplines_in_group2P_ed_fis), 0) + 
			IFNULL((negative_class_ratio2P_ingles * disciplines_in_group2P_ingles), 0) + 
			IFNULL((negative_class_ratio2P_ling_estrang * disciplines_in_group2P_ling_estrang), 0) +  
			IFNULL((negative_class_ratio2P_matematica * disciplines_in_group2P_matematica), 0) + 
			IFNULL((negative_class_ratio2P_portugues * disciplines_in_group2P_portugues), 0))/ 
			NULLIF(IFNULL(disciplines_in_group2P_art_tecn, 0) +
			IFNULL(disciplines_in_group2P_cienc_fis_nat, 0) + 
			IFNULL(disciplines_in_group2P_cienc_soc_huma, 0) +
			IFNULL(disciplines_in_group2P_ed_fis, 0) +
			IFNULL(disciplines_in_group2P_ingles, 0) +
			IFNULL(disciplines_in_group2P_ling_estrang, 0)+
			IFNULL(disciplines_in_group2P_matematica, 0) +
			IFNULL(disciplines_in_group2P_portugues, 0), 0) as negative_class_ratio_2P,
			# ratio of negative disciplines in 3P
			(IFNULL((negative_class_ratio3P_art_tecn * disciplines_in_group3P_art_tecn), 0) + 
			IFNULL((negative_class_ratio3P_cienc_fis_nat * disciplines_in_group3P_cienc_fis_nat), 0) + 
			IFNULL((negative_class_ratio3P_cienc_soc_huma * disciplines_in_group3P_cienc_soc_huma), 0) + 
			IFNULL((negative_class_ratio3P_ed_fis * disciplines_in_group3P_ed_fis), 0) + 
			IFNULL((negative_class_ratio3P_ingles * disciplines_in_group3P_ingles), 0) + 
			IFNULL((negative_class_ratio3P_ling_estrang * disciplines_in_group3P_ling_estrang), 0) +  
			IFNULL((negative_class_ratio3P_matematica * disciplines_in_group3P_matematica), 0) + 
			IFNULL((negative_class_ratio3P_portugues * disciplines_in_group3P_portugues), 0))/ 
			NULLIF(IFNULL(disciplines_in_group3P_art_tecn, 0) +
			IFNULL(disciplines_in_group3P_cienc_fis_nat, 0) + 
			IFNULL(disciplines_in_group3P_cienc_soc_huma, 0) +
			IFNULL(disciplines_in_group3P_ed_fis, 0) +
			IFNULL(disciplines_in_group3P_ingles, 0) +
			IFNULL(disciplines_in_group3P_ling_estrang, 0) +
			IFNULL(disciplines_in_group3P_matematica, 0) +
			IFNULL(disciplines_in_group3P_portugues, 0), 0) as negative_class_ratio_3P,
			# ratio of negative disciplines in 1S
			(IFNULL((negative_class_ratio1S_art_tecn * disciplines_in_group1S_art_tecn), 0) + 
			IFNULL((negative_class_ratio1S_cienc_fis_nat * disciplines_in_group1S_cienc_fis_nat), 0) + 
			IFNULL((negative_class_ratio1S_cienc_soc_huma * disciplines_in_group1S_cienc_soc_huma), 0) + 
			IFNULL((negative_class_ratio1S_ed_fis * disciplines_in_group1S_ed_fis), 0) + 
			IFNULL((negative_class_ratio1S_ingles * disciplines_in_group1S_ingles), 0) + 
			IFNULL((negative_class_ratio1S_ling_estrang * disciplines_in_group1S_ling_estrang), 0) +  
			IFNULL((negative_class_ratio1S_matematica * disciplines_in_group1S_matematica), 0) + 
			IFNULL((negative_class_ratio1S_portugues * disciplines_in_group1S_portugues), 0))/ 
			NULLIF(IFNULL(disciplines_in_group1S_art_tecn, 0) + 
			IFNULL(disciplines_in_group1S_cienc_fis_nat, 0) + 
			IFNULL(disciplines_in_group1S_cienc_soc_huma, 0) +
			IFNULL(disciplines_in_group1S_ed_fis, 0) +
			IFNULL(disciplines_in_group1S_ingles, 0) +
			IFNULL(disciplines_in_group1S_ling_estrang, 0) +
			IFNULL(disciplines_in_group1S_matematica, 0) +
			IFNULL(disciplines_in_group1S_portugues, 0), 0) as negative_class_ratio_1S,
			# ratio of negative nuclear disciplines in 1P
			((negative_class_ratio1P_matematica * disciplines_in_group1P_matematica) + 
			(negative_class_ratio1P_portugues * disciplines_in_group1P_portugues))/ 
			NULLIF(disciplines_in_group1P_matematica +
			disciplines_in_group1P_portugues, 0) as negative_class_ratio_nuclear_1P,
			# ratio of negative nuclear disciplines in 2P
			((negative_class_ratio2P_matematica * disciplines_in_group2P_matematica) + 
			(negative_class_ratio2P_portugues * disciplines_in_group2P_portugues))/ 
			NULLIF(disciplines_in_group2P_matematica +
			disciplines_in_group2P_portugues, 0) as negative_class_ratio_nuclear_2P,
			# ratio of negative nuclear disciplines in 3P
			((negative_class_ratio3P_matematica * disciplines_in_group3P_matematica) + 
			(negative_class_ratio3P_portugues * disciplines_in_group3P_portugues))/ 
			NULLIF(disciplines_in_group3P_matematica +
			disciplines_in_group3P_portugues,0) as negative_class_ratio_nuclear_3P,
			# ratio of negative nuclear disciplines in 1S
			((negative_class_ratio1S_matematica * disciplines_in_group1S_matematica) + 
			(negative_class_ratio1S_portugues * disciplines_in_group1S_portugues))/ 
			NULLIF(disciplines_in_group1S_matematica +
			disciplines_in_group1S_portugues, 0) as negative_class_ratio_nuclear_1S,
			# ratio of negative non-nuclear disciplines in 1P
			(IFNULL((negative_class_ratio1P_art_tecn * disciplines_in_group1P_art_tecn), 0) + 
			IFNULL((negative_class_ratio1P_cienc_fis_nat * disciplines_in_group1P_cienc_fis_nat), 0) + 
			IFNULL((negative_class_ratio1P_cienc_soc_huma * disciplines_in_group1P_cienc_soc_huma), 0) + 
			IFNULL((negative_class_ratio1P_ed_fis * disciplines_in_group1P_ed_fis), 0) + 
			IFNULL((negative_class_ratio1P_ingles * disciplines_in_group1P_ingles), 0) + 
			IFNULL((negative_class_ratio1P_ling_estrang * disciplines_in_group1P_ling_estrang), 0))/ 
			NULLIF(IFNULL(disciplines_in_group1P_art_tecn, 0) + 
			IFNULL(disciplines_in_group1P_cienc_fis_nat, 0) + 
			IFNULL(disciplines_in_group1P_cienc_soc_huma, 0) +
			IFNULL(disciplines_in_group1P_ed_fis, 0) +
			IFNULL(disciplines_in_group1P_ingles, 0) +
			IFNULL(disciplines_in_group1P_ling_estrang, 0), 0) as negative_class_ratio_not_nuclear_1P, 
			# ratio of negative non-nuclear disciplines in 2P
			(IFNULL((negative_class_ratio2P_art_tecn * disciplines_in_group2P_art_tecn), 0) + 
			IFNULL((negative_class_ratio2P_cienc_fis_nat * disciplines_in_group2P_cienc_fis_nat), 0) + 
			IFNULL((negative_class_ratio2P_cienc_soc_huma * disciplines_in_group2P_cienc_soc_huma), 0) + 
			IFNULL((negative_class_ratio2P_ed_fis * disciplines_in_group2P_ed_fis), 0) + 
			IFNULL((negative_class_ratio2P_ingles * disciplines_in_group2P_ingles), 0) + 
			IFNULL((negative_class_ratio2P_ling_estrang * disciplines_in_group2P_ling_estrang), 0))/ 
			NULLIF(IFNULL(disciplines_in_group2P_art_tecn, 0) + 
			IFNULL(disciplines_in_group2P_cienc_fis_nat, 0) + 
			IFNULL(disciplines_in_group2P_cienc_soc_huma, 0) +
			IFNULL(disciplines_in_group2P_ed_fis, 0) +
			IFNULL(disciplines_in_group2P_ingles, 0) +
			IFNULL(disciplines_in_group2P_ling_estrang, 0), 0) as negative_class_ratio_not_nuclear_2P,   
			# ratio of negative non-nuclear disciplines in 3P
			(IFNULL((negative_class_ratio3P_art_tecn * disciplines_in_group3P_art_tecn), 0) + 
			IFNULL((negative_class_ratio3P_cienc_fis_nat * disciplines_in_group3P_cienc_fis_nat), 0) + 
			IFNULL((negative_class_ratio3P_cienc_soc_huma * disciplines_in_group3P_cienc_soc_huma), 0) + 
			IFNULL((negative_class_ratio3P_ed_fis * disciplines_in_group3P_ed_fis), 0) + 
			IFNULL((negative_class_ratio3P_ingles * disciplines_in_group3P_ingles), 0) + 
			IFNULL((negative_class_ratio3P_ling_estrang * disciplines_in_group3P_ling_estrang), 0))/ 
			NULLIF(IFNULL(disciplines_in_group3P_art_tecn, 0) + 
			IFNULL(disciplines_in_group3P_cienc_fis_nat, 0) + 
			IFNULL(disciplines_in_group3P_cienc_soc_huma, 0) +
			IFNULL(disciplines_in_group3P_ed_fis, 0) +
			IFNULL(disciplines_in_group3P_ingles, 0) +
			IFNULL(disciplines_in_group3P_ling_estrang, 0), 0) as negative_class_ratio_not_nuclear_3P,  
			# ratio of negative non-nuclear disciplines in 1S
			(IFNULL((negative_class_ratio1S_art_tecn * disciplines_in_group1S_art_tecn), 0) + 
			IFNULL((negative_class_ratio1S_cienc_fis_nat * disciplines_in_group1S_cienc_fis_nat), 0) + 
			IFNULL((negative_class_ratio1S_cienc_soc_huma * disciplines_in_group1S_cienc_soc_huma), 0) + 
			IFNULL((negative_class_ratio1S_ed_fis * disciplines_in_group1S_ed_fis), 0) + 
			IFNULL((negative_class_ratio1S_ingles * disciplines_in_group1S_ingles), 0) + 
			IFNULL((negative_class_ratio1S_ling_estrang * disciplines_in_group1S_ling_estrang), 0))/ 
			NULLIF(IFNULL(disciplines_in_group1S_art_tecn, 0) + 
			IFNULL(disciplines_in_group1S_cienc_fis_nat, 0) + 
			IFNULL(disciplines_in_group1S_cienc_soc_huma, 0) +
			IFNULL(disciplines_in_group1S_ed_fis, 0) +
			IFNULL(disciplines_in_group1S_ingles, 0) +
			IFNULL(disciplines_in_group1S_ling_estrang, 0), 0) as negative_class_ratio_not_nuclear_1S, 
			class1P_art_tecn,
			class1P_cienc_fis_nat,
			class1P_cienc_soc_huma,
			class1P_ed_fis,
			class1P_ingles,
			class1P_ling_estrang,
			class1P_matematica,
			class1P_outros,
			class1P_portugues,
			class1S_art_tecn,
			class1S_cienc_fis_nat,
			class1S_cienc_soc_huma,
			class1S_ed_fis,
			class1S_ingles,
			class1S_ling_estrang,
			class1S_matematica,
			class1S_outros,
			class1S_portugues,
			class2P_art_tecn,
			class2P_cienc_fis_nat,
			class2P_cienc_soc_huma,
			class2P_ed_fis,
			class2P_ingles,
			class2P_ling_estrang,
			class2P_matematica,
			class2P_outros,
			class2P_portugues,
			class3P_art_tecn,
			class3P_cienc_fis_nat,
			class3P_cienc_soc_huma,
			class3P_ed_fis,
			class3P_ingles,
			class3P_ling_estrang,
			class3P_matematica,
			class3P_outros,
			class3P_portugues
	from atb2.avaliacao_singlerow_discipline_group_pivot
	) calcul

