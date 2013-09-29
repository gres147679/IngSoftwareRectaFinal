        insert into EMPRESA values
        (12345678,'MOCEL');
        
        insert into CLIENTE values (22714709,'Gustavo El Khoury',
        'Urb. Monte Elena Qta. Santa Teresa');
        
        insert into PRODUCTO values
        ('CBZ27326','iPhone 4S','12345678',22714709);
        
        insert into SERVICIO values
        (1001,'Segundos a MOCEL',0.15,FALSE);
        
        insert into PLAN values
        (3002,'Mixto Plus','Este fabuloso plan incluye todos los servicios, y 
        tarifas para excesos',211,311,'postpago');
        
        insert into INCLUYE values
        (3002,1001,0.1,100);
        
        insert into AFILIA values
        ('CBZ27326',3002,'paquete');
        
        insert into CONSUME values(
        DEFAULT,'CBZ27326',1001,current_date,20);
        insert into CONSUME values(
        DEFAULT,'CBZ27326',1001,current_date,20);
        insert into CONSUME values(
        DEFAULT,'CBZ27326',1001,current_date,20);
        insert into CONSUME values(
        DEFAULT,'CBZ27326',1001,current_date,20);
        insert into CONSUME values(
        DEFAULT,'CBZ27326',1001,current_date,20);
        insert into CONSUME values(
        DEFAULT,'CBZ27326',1001,current_date,20);
        
        insert into CONSUME values(
        DEFAULT,'CBZ27326',1001,current_date-45,20);
