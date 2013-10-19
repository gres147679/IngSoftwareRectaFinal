CREATE OR REPLACE FUNCTION existePlanPrepago()
RETURNS TRIGGER AS $existePlanPrepago$  
  BEGIN
    IF EXISTS (SELECT * 
              FROM ACTIVA AS origen
              WHERE NEW.numserie = origen.numserie) THEN RETURN NULL;
    END IF;
    RETURN NEW;
    
  END;
$existePlanPrepago$ LANGUAGE plpgsql;
 
CREATE OR REPLACE FUNCTION existePlanPostpago()
RETURNS TRIGGER AS $existePlanPostpago$
  BEGIN

    IF EXISTS (SELECT * 
              FROM AFILIA AS origen
              WHERE NEW.numserie = origen.numserie) THEN RETURN NULL;
    END IF;
    RETURN NEW;
  END;
$existePlanPostpago$ LANGUAGE plpgsql;
  
CREATE TRIGGER existePlanPrepago
BEFORE INSERT ON ACTIVA FOR EACH ROW 
EXECUTE PROCEDURE existePlanPostpago();
  
CREATE TRIGGER existePlanPostpago 
BEFORE INSERT ON AFILIA FOR EACH ROW 
EXECUTE PROCEDURE existePlanPrepago();


/*
 * Triggers que se encargan de la segunda restricción explícita:
 * 2. Si un servicio es único, el atributo cantidad en cada instancia de las
 * interrelaciones consume, contiene e incluye debe valer 1
 */
CREATE OR REPLACE FUNCTION servicioEsUnico1() 
RETURNS TRIGGER AS $servicioEsUnico1$
  BEGIN
    IF (SELECT unico 
    FROM SERVICIO AS origen 
    WHERE origen.codserv=NEW.codserv) THEN
      IF NEW.cantidad = 1 AND NOT EXISTS (select * from CONSUME AS origen 
      where origen.numSerie = NEW.numSerie AND origen.codserv = NEW.codserv)
        THEN RETURN NEW;
        ELSE RETURN NULL;
      END IF;
    END IF;
    RETURN NEW;
  END;
$servicioEsUnico1$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION servicioEsUnico2() 
RETURNS TRIGGER AS $servicioEsUnico2$
  BEGIN
    IF (SELECT unico 
    FROM SERVICIO AS origen 
    WHERE origen.codserv=NEW.codserv) THEN
      IF NEW.cantidad = 1 AND NOT EXISTS(select * from INCLUYE AS 
      origen where origen.codserv = NEW.codserv AND origen.codplan =
NEW.codplan)
      THEN RETURN NEW;
      ELSE RETURN NULL;
      END IF;
    END IF;
    RETURN NEW;
  END;
$servicioEsUnico2$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION servicioEsUnico3() 
RETURNS TRIGGER AS $servicioEsUnico3$
  BEGIN
    IF (SELECT unico 
    FROM SERVICIO AS origen 
    WHERE origen.codserv=NEW.codserv) THEN
      IF NEW.cantidad = 1 AND NOT EXISTS(select * from CONTIENE AS 
      origen where origen.codpaq = NEW.codpaq AND origen.codserv = NEW.codserv)
      THEN RETURN NEW;
      ELSE RETURN NULL;
      END IF;
    END IF;
    RETURN NEW;
  END;
$servicioEsUnico3$ LANGUAGE plpgsql;
  
CREATE TRIGGER servicioEsUnico1 
BEFORE INSERT OR UPDATE ON CONSUME FOR EACH ROW 
EXECUTE PROCEDURE servicioEsUnico1();

CREATE TRIGGER servicioEsUnico2 
BEFORE INSERT OR UPDATE ON INCLUYE FOR EACH ROW 
EXECUTE PROCEDURE servicioEsUnico2();

CREATE TRIGGER servicioEsUnico3 
BEFORE INSERT OR UPDATE ON CONTIENE FOR EACH ROW 
EXECUTE PROCEDURE servicioEsUnico3();


/*
 * Trigger que se encarga de la cuarta restricción explícita y la quinta
 * 4. Un producto no puede consumir ningún servicio (aparecer en la
 * interrelación consume) si no está afiliado algún plan postpago o prepago
 * 5. Un producto no puede consumir ningún servicio si no está afiliado algún
 * plan prepago con saldo positivo
 */
CREATE OR REPLACE FUNCTION saldoPositivo() 
RETURNS TRIGGER AS $saldoPositivo$
DECLARE 
  saldo_actual real;
  cantidad_consumida int;
  cantidad_actual int;
  tarifa_plan real;
  cobro real;
  cantidad_incluida int;
  
  BEGIN
    
--     Significa que está afiliado a un plan postpago
    IF EXISTS (SELECT *
               FROM AFILIA
               WHERE numserie = NEW.numserie) THEN RETURN NEW;
    
    ELSE
      
      saldo_actual := (SELECT saldo
                       FROM ACTIVA
                       WHERE numserie = NEW.numserie);
    
      SELECT cantidad, tarifa INTO cantidad_incluida, tarifa_plan
      FROM INCLUYE NATURAL JOIN ACTIVA
      WHERE codserv = NEW.codserv AND numserie = NEW.numserie;
      
--       Si existe algún paquete con ese servicio incluido
      IF EXISTS (SELECT *
                 FROM CONTRATA NATURAL JOIN CONTIENE
                 WHERE numserie = NEW.numserie AND codserv = NEW.codserv) THEN
        
        cantidad_incluida = cantidad_incluida + 
                            (SELECT cantidad
                             FROM CONTRATA NATURAL JOIN CONTIENE
                             WHERE numserie = NEW.numserie 
                              AND codserv = NEW.codserv);
      END IF;
        
      IF EXISTS (SELECT *
                 FROM CONSUME
                 WHERE numserie = NEW.numserie AND codserv = NEW.codserv 
                 AND EXTRACT(month FROM fecha) = EXTRACT(month FROM NEW.fecha)
                 AND EXTRACT(year FROM fecha) = EXTRACT(year FROM NEW.fecha)) 
        THEN
          
        SELECT SUM(cantidad) INTO cantidad_consumida
        FROM CONSUME
        WHERE numserie = NEW.numserie AND codserv = NEW.codserv 
        AND EXTRACT(month FROM fecha) = EXTRACT(month FROM NEW.fecha)
        AND EXTRACT(year FROM fecha) = EXTRACT(year FROM NEW.fecha);
        
        IF cantidad_consumida >= cantidad_incluida THEN
          cobro := NEW.cantidad * tarifa_plan;
          IF saldo_actual < cobro THEN RETURN NULL;
          ELSE RETURN NEW;
          END IF;
          
        ELSE
          cantidad_actual := cantidad_incluida - cantidad_consumida;
          IF NEW.cantidad <= cantidad_actual THEN RETURN NEW;
          ELSE
            cobro := (NEW.cantidad - cantidad_actual) * tarifa_plan;
            IF saldo_actual < cobro THEN RETURN NULL;
            ELSE RETURN NEW;
            END IF;
          END IF;
        END IF;
          
      ELSE
      
        IF cantidad_incluida >= NEW.cantidad THEN RETURN NEW;
        ELSE
          cobro := (NEW.cantidad - cantidad_incluida) * tarifa_plan;
          IF saldo_actual < cobro THEN RETURN NULL;
          ELSE RETURN NEW;
          END IF;
        END IF;
        
      END IF;
        
    END IF;

  END;
$saldoPositivo$ LANGUAGE plpgsql;

CREATE TRIGGER saldoPositivo
BEFORE INSERT ON CONSUME
FOR EACH ROW EXECUTE PROCEDURE saldoPositivo();


/*
 * Trigger que maneja la restricción explícita 7:
 * Un producto no puede consumir un servicio que no esté incluido en el plan al
 * que está afiliado o en algún paquete que haya contratado.
 */
CREATE OR REPLACE FUNCTION consumoCoherente()
RETURNS TRIGGER AS $consumoCoherente$
  
  BEGIN

-- Si su plan lo incluye, acepta
    IF EXISTS (SELECT *
               FROM ACTIVA NATURAL JOIN INCLUYE
               WHERE numserie = NEW.numserie AND codserv = NEW.codserv)
       OR
       
       EXISTS (SELECT *
               FROM AFILIA NATURAL JOIN INCLUYE
               WHERE numserie = NEW.numserie AND codserv = NEW.codserv)
       
       THEN RETURN NEW;
  
    ELSE 
   
      IF (EXISTS (SELECT *
                  FROM ACTIVA 
                  WHERE numserie = NEW.numserie)
         OR
      
         EXISTS (SELECT *
                 FROM AFILIA
                 WHERE numserie = NEW.numserie))
          
         AND EXISTS (SELECT *
                     FROM CONTRATA NATURAL JOIN CONTIENE
                     WHERE numserie = NEW.numserie AND codserv = NEW.codserv)
          THEN RETURN NEW;
      ELSE 
        RAISE WARNING 'INVE001: No se puede agregar un consumo si no hay un plan o paquete que lo respalde';
        RETURN NULL;
      END IF;
    END IF;
      
  END;
$consumoCoherente$ LANGUAGE plpgsql;

CREATE TRIGGER consumoCoherente
BEFORE INSERT ON CONSUME
FOR EACH ROW EXECUTE PROCEDURE consumoCoherente();


/*
 * Trigger que maneja la restricción de traducción 3 y 4:
 * 3. Toda instancia de plan está en plan prepago o plan postpago, pero no en
 * ambas.
 * 4. Todo elemento de las relaciones plan prepago y plan postpago, están una
 * vez en plan.
 */
CREATE OR REPLACE FUNCTION autoFillPlan()
RETURNS TRIGGER AS $autoFillPlan$
  BEGIN
    IF (NEW.tipo = 'prepago') THEN
      INSERT INTO PLAN_PREPAGO VALUES (NEW.codplan);
    ELSE
      INSERT INTO PLAN_POSTPAGO VALUES (NEW.codplan);
    END IF;
    RETURN NULL;
  END;
$autoFillPlan$ LANGUAGE plpgsql;

CREATE TRIGGER autoFillPlan
AFTER INSERT ON PLAN
FOR EACH ROW EXECUTE PROCEDURE autoFillPlan();


/*
 * Trigger que maneja la restricción de traducción 7:
 * 7. Todo servicio es parte de por lo menos un paquete.
 */
CREATE OR REPLACE FUNCTION autoCreaPaquete() 
RETURNS TRIGGER AS $autoCreaPaquete$
DECLARE
  costoServ integer;
  saldoAf integer;
  canti integer;
  incluido integer;
  BEGIN
    IF (NEW.unico) THEN
      INSERT INTO PAQUETE VALUES
      (NEW.codserv,'Paquete ' || NEW.nombreserv,NEW.costo);
      INSERT INTO CONTIENE VALUES
      (NEW.codserv,NEW.codserv,1);
    END IF;
    RETURN NEW;
  END;  
$autoCreaPaquete$ LANGUAGE plpgsql;

CREATE TRIGGER autoCreaPaquete
AFTER INSERT ON SERVICIO FOR EACH ROW 
EXECUTE PROCEDURE autoCreaPaquete();

--------------------------------------------------------------------------------

/*
 * Trigger que actualiza el saldo prepago
 */
CREATE OR REPLACE FUNCTION actualizaSaldo() 
RETURNS TRIGGER AS $actualizaSaldo$
DECLARE
    
  cantidad_incluida_paquete integer;
  cantidad_incluida_plan integer;
  cantidad_incluida_total integer;
  cantidad_incluida integer;
  cantidad_total_consumida integer;
  cantidad_consumida integer;
  costo_servicio real;
  costo_extra real;
  saldo_actual real;
  saldo_nuevo real;
    
  BEGIN
  
    -- Si tiene un plan postpago
    
    IF EXISTS (SELECT *
               FROM AFILIA
               WHERE numserie = NEW.numserie) THEN RETURN NULL;
    END IF;
    
    cantidad_incluida_paquete := (SELECT cantidad
                                 FROM PRODUCTO NATURAL JOIN CONTRATA NATURAL JOIN CONTIENE
                                 WHERE numserie = NEW.numserie AND codserv = NEW.codserv);
                                 
    if cantidad_incluida_paquete is null then cantidad_incluida_paquete := 0; end if;
                                 
    cantidad_incluida_plan := (SELECT cantidad
                               FROM PRODUCTO NATURAL JOIN ACTIVA NATURAL JOIN INCLUYE
                               WHERE numserie = NEW.numserie AND codserv = NEW.codserv);
    
    if cantidad_incluida_plan is null then cantidad_incluida_plan := 0; end if;
    
    cantidad_incluida := cantidad_incluida_paquete + cantidad_incluida_plan;
    
    -- Ahora vemos los consumos hechos
    
    SELECT SUM(cantidad) INTO cantidad_total_consumida
    FROM CONSUME
    WHERE numserie = NEW.numserie AND codserv = NEW.codserv 
        AND EXTRACT(month FROM fecha) = EXTRACT(month FROM NEW.fecha)
        AND EXTRACT(year FROM fecha) = EXTRACT(year FROM NEW.fecha);
    
    cantidad_consumida := NEW.cantidad;
    cantidad_total_consumida := cantidad_total_consumida - cantidad_consumida;
    cantidad_incluida_total := cantidad_incluida - cantidad_total_consumida;
        
    costo_servicio := (SELECT tarifa 
                       FROM PRODUCTO NATURAL JOIN ACTIVA NATURAL JOIN INCLUYE
                       WHERE numserie = NEW.numserie AND codserv = NEW.codserv);

    IF cantidad_incluida_total <= 0 THEN
        costo_extra := costo_servicio*cantidad_consumida;
    ELSE
        cantidad_total_consumida := cantidad_total_consumida + cantidad_consumida;
        IF cantidad_total_consumida > cantidad_incluida THEN
            costo_extra := costo_servicio*(cantidad_total_consumida-cantidad_incluida);
        ELSE costo_extra := 0;
        END IF;
    END IF;
        
    saldo_actual := (SELECT saldo
                     FROM ACTIVA
                     WHERE numserie = NEW.numserie);                     
                        
    saldo_nuevo := saldo_actual-costo_extra;
    
    UPDATE ACTIVA
    SET saldo = saldo_nuevo
    WHERE numserie = NEW.numserie;
    
    RETURN NEW;
    
  END;
$actualizaSaldo$ LANGUAGE plpgsql;

CREATE TRIGGER actualizaSaldo 
AFTER INSERT ON CONSUME FOR EACH ROW 
EXECUTE PROCEDURE actualizaSaldo();


/*
 * Trigger que actualiza el saldo de un producto prepago despues
 * de realizar una recarga.
 */
CREATE OR REPLACE FUNCTION realizaRecarga() 
RETURNS TRIGGER AS $realizaRecarga$
DECLARE 
  saldo_actual real;
  cantidad_total real;
  
  BEGIN
    
--     Significa que está afiliado a un plan postpago
    IF EXISTS (SELECT *
               FROM AFILIA
               WHERE numserie = NEW.numserie) THEN RETURN NEW;
    
    ELSE
      
      saldo_actual := (SELECT saldo
                       FROM ACTIVA
                       WHERE numserie = NEW.numserie);

      cantidad_total := NEW.cantidad + saldo_actual; 
      
      UPDATE ACTIVA
      SET saldo = cantidad_total
      WHERE numserie = NEW.numserie;
    
    END IF;
    
    return NEW;

  END;
$realizaRecarga$ LANGUAGE plpgsql;

CREATE TRIGGER realizaRecarga
AFTER INSERT ON RECARGA
FOR EACH ROW EXECUTE PROCEDURE realizaRecarga();


-- Trigger de maximo un plan
CREATE OR REPLACE FUNCTION existePlan()
RETURNS TRIGGER AS $existePlan$
  BEGIN

    IF EXISTS (SELECT * 
               FROM AFILIA
               WHERE NEW.numserie = numserie) 
        OR

        EXISTS (SELECT * 
               FROM ACTIVA
               WHERE NEW.numserie = numserie) 
               
        THEN RETURN NULL;
    END IF;
    RETURN NEW;
  END;
$existePlan$ LANGUAGE plpgsql;
  
CREATE TRIGGER existePlan1
BEFORE INSERT ON ACTIVA FOR EACH ROW 
EXECUTE PROCEDURE existePlan();

CREATE TRIGGER existePlan2
BEFORE INSERT ON AFILIA FOR EACH ROW 
EXECUTE PROCEDURE existePlan();