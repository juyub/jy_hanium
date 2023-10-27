CREATE TABLE detected_faces (
    face_id NUMBER,
    gender VARCHAR2(10),
    age VARCHAR2(10),
    detect_time TIMESTAMP
);

select * from detected_faces;

drop table detected_faces;

SELECT MAX(face_id) FROM detected_faces;

 SELECT 
     age,
     gender,
     COUNT(*) as a_g_count
 FROM detected_faces
 WHERE TRUNC(detect_time) BETWEEN TO_DATE('2023-10-01', 'YYYY-MM-DD') 
                              AND TO_DATE('2023-10-19', 'YYYY-MM-DD')
 GROUP BY age,gender
 ORDER BY age,gender;
