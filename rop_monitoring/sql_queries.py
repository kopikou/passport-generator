from datetime import datetime

MARKS_QUERY = f"""
    SELECT 
        cs.id AS student_id,
        su.name AS subject_name, 
        su.isege AS is_ege,
        su.alternative AS is_alternative,
        CAST(ss.mark AS FLOAT) as mark
    FROM  dbo.stud2subject AS ss 
    LEFT OUTER JOIN dbo.cl$subject AS su ON su.id = ss.csubject 
    LEFT OUTER JOIN dbo.catstud AS cs ON cs.id = ss.cstud 
    LEFT OUTER JOIN dbo.catadmission AS ca ON ca.id = cs.cadmission
    WHERE 
        CAST(ss.mark AS FLOAT) > 0
        AND ca.cadmkind IN (1, 2, 3)
        AND ca.cfac NOT IN (40)
        AND cs.cset IN (1, 2, 3)
        AND cs.cstudstate IN (1, 10, 21, 22, 12, 31, 5, 13, 27, 28, 32)
        AND ca.cfob IN (1, 2)
        AND YEAR(ca.dateend) >= {datetime.now().year} - 1
    GROUP BY
        cs.id,
        su.name, 
        su.isege,
        su.alternative,
        CAST(ss.mark AS FLOAT)
    ORDER BY 1, 3, 2
"""

STUDENTS_QUERY = f"""
    SELECT 
        cs.id AS student_id, 
        cs.name AS student_name, 
        cf.name AS faculty_name, 
        cs.cadmission AS admission_id, 
        ca.name as admission_name, 
        cs.yearpost AS student_admission_year, 
        ca.cfob AS education_form, 
        convert(varchar, ca.dateend, 104) AS admission_date_end,
        dog_c.nomer as student_dog_cel, 
        dog_c.dog_inedu as student_dog_in_edu,
        dog_c.cstat as student_dog_state,
        cs.cstudstate AS student_state, 
        ca.yr AS admission_year, 
        ca.abbr AS admission_abbr, 
        direction.full_name AS direction_name,
        direction.code AS direction_code, 
        cs.cset AS student_set,
        CASE WHEN cs.yearpost = ca.yr THEN 1 ELSE 0 END AS that_year_student,
        CASE WHEN cs.cset IN (1, 2, 6) THEN 'b' WHEN cs.cset IN (3, 7) THEN 'c' ELSE NULL END AS student_set_name,
        pers.name AS admission_rop,
        pers.id AS admission_rop_id,
        ca.uchPeriod AS admission_period
    FROM dbo.catstud cs 
    LEFT JOIN dbo.catadmission ca ON ca.id = cs.cadmission
    LEFT JOIN dbo.uchplan_plan pl ON pl.id = ca.cuchplan
    LEFT JOIN dbo.catperson pers ON pers.id = pl.cperson
    LEFT JOIN dbo.catfaculty cf ON cf.id = ca.cfac
    LEFT JOIN dbo.catdogcelev dog_c ON cs.id = dog_c.cstud
    LEFT JOIN (
        SELECT a.id,
            CASE 
                WHEN a.cadmkind=1 THEN ISNULL(sp.code+' '+sp.name, dir.cod+' '+dir.name)
                WHEN a.cadmkind=2 THEN COALESCE(sp1.code+' '+sp1.name, dir.cod+' '+dir.name,sp.code+' '+sp.name)
                WHEN a.cadmkind=3 THEN ISNULL(sp.code+' '+sp.name, dir.cod+' '+dir.name)
                WHEN a.cadmkind=4 THEN ISNULL(dir.cod+' '+dir.name, sp.code+' '+sp.name)
                WHEN a.cadmkind=5 THEN ISNULL(sp.code+' '+sp.name, dir.cod+' '+dir.name)
                ELSE sp.code+' '+sp.name
            END AS full_name,
            CASE 
                WHEN a.cadmkind=1 THEN ISNULL(sp.code, dir.cod)
                WHEN a.cadmkind=2 THEN COALESCE(sp1.code, dir.cod,sp.code)
                WHEN a.cadmkind=3 THEN ISNULL(sp.code, dir.cod)
                WHEN a.cadmkind=4 THEN ISNULL(dir.cod, sp.code)
                WHEN a.cadmkind=5 THEN ISNULL(sp.code, dir.cod)
                ELSE sp.code
            END AS code
        FROM catadmission a
        LEFT JOIN [cl$spec] sp ON sp.id = a.cspec
        LEFT JOIN [cl$spec] sp1 ON sp1.id = a.cprofili
        LEFT JOIN [cl$direction] dir ON dir.id = a.cdirection
        WHERE a.cadmkind < 6
    ) direction ON direction.id = cs.cadmission
    WHERE 
    cs.cstudstate IN (1, 10, 21, 22, 12, 31, 5, 13, 27, 28, 32)
    AND YEAR(ca.dateend) >= {datetime.now().year} - 1
    AND cs.name IS NOT NULL
    AND ca.cfob IN (1, 2)
    ORDER BY 3, 5, 2
"""

ORDERS_QUERY = f"""
    SELECT 
        o.ddat AS order_date, 
        f.name AS comment,
        f.val as admission_id, 
        ois.cstud AS student_id
    FROM dbo.order_items oi
    LEFT JOIN dbo.order_fields f ON f.citem = oi.id
    LEFT JOIN dbo.catorder o ON o.id = oi.corder
    LEFT JOIN dbo.orderitem2stud ois ON ois.citem = oi.id
    LEFT JOIN dbo.catstud cs ON cs.id = ois.cstud
    LEFT JOIN dbo.catadmission ca ON ca.id = cs.cadmission
    WHERE
        oi.corder_type IN (260518, 268613, 684369, 935108, 1604347, 1604347, 2082658, 2082687, 2082688, 2082688, 2082688, 2082734, 2082801, 2082861)
        AND cs.cstudstate IN (1, 5, 10, 12, 13, 21, 22, 27, 28, 31, 32)
        AND YEAR(ca.dateend) >= {datetime.now().year} - 1
        AND cs.name IS NOT NULL
        AND o.ddat IS NOT NULL
	GROUP BY o.ddat, f.name, f.val, ois.cstud
    ORDER BY 1 ASC, 4 ASC
"""

ADMISSIONS_QUERY = f"""
    SELECT 
        ca.id AS admission_id, 
        ca.abbr AS admission_abbr, 
        ca.name AS admission_name, 
        ca.yr AS admission_year, 
        convert(varchar, ca.dateend, 104) AS admission_date_end,
        cf.name AS faculty_name, 
        direction.full_name AS direction_name,
        direction.code AS direction_code,
        pers.name AS admission_rop,
        pers.id AS admission_rop_id,
        ca.uchPeriod AS admission_period,
        ca.cadmkind AS admission_kind
    FROM dbo.catadmission ca
    LEFT JOIN dbo.catfaculty cf ON cf.id = ca.cfac
    LEFT JOIN dbo.uchplan_plan pl ON pl.id = ca.cuchplan
    LEFT JOIN dbo.catperson pers ON pers.id = pl.cperson
    LEFT JOIN (
            SELECT a.id,
                CASE 
                    WHEN a.cadmkind=1 THEN ISNULL(sp.code+' '+sp.name, dir.cod+' '+dir.name)
                    WHEN a.cadmkind=2 THEN COALESCE(sp1.code+' '+sp1.name, dir.cod+' '+dir.name,sp.code+' '+sp.name)
                    WHEN a.cadmkind=3 THEN ISNULL(sp.code+' '+sp.name, dir.cod+' '+dir.name)
                    WHEN a.cadmkind=4 THEN ISNULL(dir.cod+' '+dir.name, sp.code+' '+sp.name)
                    WHEN a.cadmkind=5 THEN ISNULL(sp.code+' '+sp.name, dir.cod+' '+dir.name)
                    ELSE sp.code+' '+sp.name
                END AS full_name,
                CASE 
                    WHEN a.cadmkind=1 THEN ISNULL(sp.code, dir.cod)
                    WHEN a.cadmkind=2 THEN COALESCE(sp1.code, dir.cod,sp.code)
                    WHEN a.cadmkind=3 THEN ISNULL(sp.code, dir.cod)
                    WHEN a.cadmkind=4 THEN ISNULL(dir.cod, sp.code)
                    WHEN a.cadmkind=5 THEN ISNULL(sp.code, dir.cod)
                    ELSE sp.code
                END AS code
            FROM catadmission a
            LEFT JOIN [cl$spec] sp ON sp.id = a.cspec
            LEFT JOIN [cl$spec] sp1 ON sp1.id = a.cprofili
            LEFT JOIN [cl$direction] dir ON dir.id = a.cdirection
            WHERE a.cadmkind < 6
        ) direction ON direction.id = ca.id
    WHERE 
    YEAR(ca.dateend) >= ${datetime.now().year} - 1
    AND (ca.cspec IS NOT NULL 
    OR ca.cprofili IS NOT NULL)
    AND ca.cfob in (1, 2)
    AND ca.cfac NOT IN (40)
    AND ca.cadmkind IN (1, 2, 3)
    AND pers.id IS NOT NULL
    ORDER BY 5, 2
"""

ORDERS_FOR_STUDENTS_WENT_TO_ACADEM_QUERY = f"""
    SELECT 
        o2s.cstud AS student_id, 
        co.id AS order_id,
		f.val AS value,
		oi.ptext AS order_text
    FROM dbo.catorder co
    LEFT JOIN dbo.order_items oi ON oi.corder = co.id
	LEFT JOIN dbo.order_fields f ON f.citem = oi.id
    LEFT JOIN dbo.orderitem2stud o2s ON o2s.citem = oi.id
    WHERE 
        oi.corder_type IN (255668, 263231, 275417, 2082794, 2082819)
        AND o2s.cstud IS NOT NULL
    ORDER BY o2s.cstud
"""

ORDERS_FOR_STUDENTS_CAME_FROM_ACADEM_QUERY = f"""
    SELECT 
        o2s.cstud AS student_id, 
        co.id AS order_id,
		f.val AS value,
		oi.ptext AS order_text
    FROM dbo.catorder co
    LEFT JOIN dbo.order_items oi ON oi.corder = co.id
	LEFT JOIN dbo.order_fields f ON f.citem = oi.id
    LEFT JOIN dbo.orderitem2stud o2s ON o2s.citem = oi.id
    WHERE 
        oi.corder_type IN (255830, 2082663, 2082795)
        AND o2s.cstud IS NOT NULL
    ORDER BY o2s.cstud
"""

ORDERS_FOR_STUDENTS_MOVED_QUERY = f"""
    SELECT 
        o2s.cstud AS student_id, 
        co.id AS order_id,
        f.val AS value,
        oi.corder_type,
        oi.ptext AS order_text
    FROM dbo.catorder co
    LEFT JOIN dbo.order_items oi ON oi.corder = co.id
    LEFT JOIN dbo.order_fields f ON f.citem = oi.id
    LEFT JOIN dbo.orderitem2stud o2s ON o2s.citem = oi.id
    WHERE 
        oi.corder_type IN (SELECT id FROM dbo.order_types WHERE name LIKE '%Перевести%' AND pattern LIKE '%полагать%')
        AND o2s.cstud IS NOT NULL
    ORDER BY o2s.cstud
"""

CELEV_DOGS_QUERY = """
    SELECT id, nomer, cstud AS student_id, cstat AS dog_state
    FROM dbo.catdogcelev 
    ORDER BY id desc
"""


NPR_QUERY = """
    SELECT cadmission,cperson FROM dbo.person2uchnagr
    WHERE ddat BETWEEN '10/09/2024' AND '10/09/2025'
"""

STUD_SOP_SUMM_QUERY = """
 SELECT LEFT(lg1.cnewgrup, LEN(lg1.cnewgrup) - 2) AS cnewgrup,
    COUNT(DISTINCT CASE WHEN '01/01/2025' BETWEEN lg1.ddate AND COALESCE(cs.dateend,'01/01/3001') THEN lg1.cstud END) +
    COUNT(DISTINCT CASE WHEN '01/07/2025' BETWEEN lg1.ddate AND COALESCE(cs.dateend,'01/01/3001') THEN lg1.cstud END) AS summa
FROM dbo.[log$studgrup] lg1
LEFT JOIN dbo.[log$studgrup] lg2 ON lg1.cnewgrup = lg2.coldgrup AND lg1.cstud = lg2.cstud
LEFT JOIN dbo.catstud cs ON cs.id = lg1.cstud
WHERE lg1.cnewgrup IS NOT NULL AND lg1.cnewgrup <> '' 
--AND '01/01/2025' BETWEEN lg1.ddate AND COALESCE(lg2.ddate, cs.dateend,'01/01/3001')
GROUP BY LEFT(lg1.cnewgrup, LEN(lg1.cnewgrup) - 2)
HAVING COUNT(DISTINCT CASE WHEN '01/01/2025' BETWEEN lg1.ddate AND COALESCE(cs.dateend,'01/01/3001') THEN lg1.cstud END) +
    COUNT(DISTINCT CASE WHEN '01/07/2025' BETWEEN lg1.ddate AND COALESCE(cs.dateend,'01/01/3001') THEN lg1.cstud END) > 0
"""

STUD_SOP_RES_QUERY = """
select cadmission, LEFT(client_group, LENGTH(client_group) - 2) AS client_group,
        (COUNT(DISTINCT CASE WHEN s.year = 2025 AND s.semestr = 2 THEN mira_id END)  +
        COUNT(DISTINCT CASE WHEN s.year = 2025 - 1 AND s.semestr = 1 THEN mira_id END)) as summa
 from sop_surveyresult
left join sop_surveydisciplineresult on sop_surveyresult.id = sop_surveydisciplineresult.survey_result_id
 left join sop_survey s on sop_surveyresult.survey_id = s.id
where survey_id in (select id from sop_survey where (year=2025 and semestr=2) or (year=(select 2025 - 1) and semestr=1))
group by cadmission, LEFT(client_group, LENGTH(client_group) - 2)
"""

