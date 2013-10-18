CREATE OR REPLACE FUNCTION existePlanPrepago()
RETURNS TRIGGER AS $existePlanPrepago$
  BEGIN
    IF EXISTS (SELECT * 
              FROM "WebAccess_activa" AS origen
              WHERE NEW.numserie_id = origen.numserie_id) THEN RETURN NULL;
    END IF;
    RETURN NEW;
    
  END;
$existePlanPrepago$ LANGUAGE plpgsql;

CREATE TRIGGER existePlanPostpago 
BEFORE INSERT ON "WebAccess_afilia" FOR EACH ROW 
EXECUTE PROCEDURE existePlanPrepago();


CREATE OR REPLACE FUNCTION existePlanPostpago()
RETURNS TRIGGER AS $existePlanPostpago$
  BEGIN

    IF EXISTS (SELECT * 
              FROM "WebAccess_afilia" AS origen
              WHERE NEW.numserie_id = origen.numserie_id) THEN RETURN NULL;
    END IF;
    RETURN NEW;
  END;
$existePlanPostpago$ LANGUAGE plpgsql;

CREATE TRIGGER existePlanPrepago
BEFORE INSERT ON "WebAccess_activa" FOR EACH ROW 
EXECUTE PROCEDURE existePlanPostpago();


CREATE OR REPLACE FUNCTION servicioEsUnico1() 
RETURNS TRIGGER AS $servicioEsUnico1$
  BEGIN
    IF (SELECT unico
    FROM "WebAccess_servicio" AS origen 
    WHERE origen.codserv=NEW.codserv_id) THEN
      IF NEW.cantidad = 1 AND NOT EXISTS (select * from "WebAccess_consume" AS origen 
      where origen.numserie_id = NEW.numserie_id AND origen.codserv_id = NEW.codserv_id)
        THEN RETURN NEW;
        ELSE RETURN NULL;
      END IF;
    END IF;
    RETURN NEW;
  END;
$servicioEsUnico1$ LANGUAGE plpgsql;

CREATE TRIGGER servicioEsUnico1 
BEFORE INSERT OR UPDATE ON "WebAccess_consume" FOR EACH ROW 
EXECUTE PROCEDURE servicioEsUnico1();


CREATE OR REPLACE FUNCTION servicioEsUnico2() 
RETURNS TRIGGER AS $servicioEsUnico2$
  BEGIN
    IF (SELECT unico 
    FROM "WebAccess_servicio" AS origen 
    WHERE origen.codserv=NEW.codserv_id) THEN
      IF NEW.cantidad = 1 AND NOT EXISTS(select * from "WebAccess_incluye" AS 
      origen where origen.codserv_id = NEW.codserv_id AND origen.codplan_id =
NEW.codplan_id)
      THEN RETURN NEW;
      ELSE RETURN NULL;
      END IF;
    END IF;
    RETURN NEW;
  END;
$servicioEsUnico2$ LANGUAGE plpgsql;

CREATE TRIGGER servicioEsUnico2 
BEFORE INSERT OR UPDATE ON "WebAccess_incluye" FOR EACH ROW 
EXECUTE PROCEDURE servicioEsUnico2();


CREATE OR REPLACE FUNCTION servicioEsUnico3() 
RETURNS TRIGGER AS $servicioEsUnico3$
  BEGIN
    IF (SELECT unico 
    FROM "WebAccess_servicio" AS origen 
    WHERE origen.codserv=NEW.codserv_id) THEN
      IF NEW.cantidad = 1 AND NOT EXISTS(select * from "WebAccess_contiene" AS 
      origen where origen.codpaq_id = NEW.codpaq_id AND origen.codserv_id = NEW.codserv_id)
      THEN RETURN NEW;
      ELSE RETURN NULL;
      END IF;
    END IF;
    RETURN NEW;
  END;
$servicioEsUnico3$ LANGUAGE plpgsql;

CREATE TRIGGER servicioEsUnico3 
BEFORE INSERT OR UPDATE ON "WebAccess_contiene" FOR EACH ROW 
EXECUTE PROCEDURE servicioEsUnico3();


CREATE OR REPLACE FUNCTION saldoPositivo() 
RETURNS TRIGGER AS $saldoPositivo$
DECLARE 
  saldo_actual double precision;
  cantidad_consumida integer;
  cantidad_actual integer;
  tarifa_plan double precision;
  cobro double precision;
  cantidad_incluida integer;
  
  BEGIN
    
    IF EXISTS (SELECT *
               FROM "WebAccess_afilia"
               WHERE numserie_id = NEW.numserie_id) THEN RETURN NEW;
    
    ELSE
      
      saldo_actual := (SELECT saldo
                       FROM "WebAccess_activa"
                       WHERE numserie_id = NEW.numserie_id);
    
      SELECT cantidad, tarifa INTO cantidad_incluida, tarifa_plan
      FROM "WebAccess_incluye" NATURAL JOIN "WebAccess_activa"
      WHERE codserv_id = NEW.codserv_id AND numserie_id = NEW.numserie_id;
      
      IF EXISTS (SELECT *
                 FROM "WebAccess_contrata" NATURAL JOIN "WebAccess_contiene"
                 WHERE numserie_id = NEW.numserie_id AND codserv_id = NEW.codserv_id) THEN
        
        cantidad_incluida = cantidad_incluida + 
                            (SELECT cantidad
                             FROM "WebAccess_contrata" NATURAL JOIN "WebAccess_contiene"
                             WHERE numserie_id = NEW.numserie_id
                              AND codserv_id = NEW.codserv_id);
      END IF;
        
      IF EXISTS (SELECT *
                 FROM "WebAccess_consume"
                 WHERE numserie_id = NEW.numserie_id AND codserv_id = NEW.codserv_id 
                 AND EXTRACT(month FROM fecha) = EXTRACT(month FROM NEW.fecha)
                 AND EXTRACT(year FROM fecha) = EXTRACT(year FROM NEW.fecha)) 
        THEN
          
        SELECT SUM(cantidad) INTO cantidad_consumida
        FROM "WebAccess_consume"
        WHERE numserie_id = NEW.numserie_id AND codserv_id = NEW.codserv_id
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
BEFORE INSERT ON "WebAccess_consume"
FOR EACH ROW EXECUTE PROCEDURE saldoPositivo();


CREATE OR REPLACE FUNCTION consumoCoherente()
RETURNS TRIGGER AS $consumoCoherente$
  
  BEGIN

    IF EXISTS (SELECT *
               FROM "WebAccess_activa" NATURAL JOIN "WebAccess_incluye"
               WHERE numserie_id = NEW.numserie_id AND codserv_id = NEW.codserv_id)
       OR
       
       EXISTS (SELECT *
               FROM "WebAccess_afilia" NATURAL JOIN "WebAccess_incluye"
               WHERE numserie_id = NEW.numserie_id AND codserv_id = NEW.codserv_id)
       
       THEN RETURN NEW;
  
    ELSE 
   
      IF (EXISTS (SELECT *
                  FROM "WebAccess_activa"
                  WHERE numserie_id = NEW.numserie_id)
         OR
      
         EXISTS (SELECT *
                 FROM "WebAccess_afilia"
                 WHERE numserie_id = NEW.numserie_id))
          
         AND EXISTS (SELECT *
                     FROM "WebAccess_contrata" NATURAL JOIN "WebAccess_contiene"
                     WHERE numserie_id = NEW.numserie_id AND codserv_id = NEW.codserv_id)
          THEN RETURN NEW;
      ELSE 
        RAISE WARNING 'INVE001: No se puede agregar un consumo si no hay un plan o paquete que lo respalde';
        RETURN NULL;
      END IF;
    END IF;
      
  END;
$consumoCoherente$ LANGUAGE plpgsql;

CREATE TRIGGER consumoCoherente
BEFORE INSERT ON "WebAccess_consume"
FOR EACH ROW EXECUTE PROCEDURE consumoCoherente();


CREATE OR REPLACE FUNCTION autoCreaPaquete() 
RETURNS TRIGGER AS $autoCreaPaquete$
DECLARE
  costoServ integer;
  saldoAf integer;
  canti integer;
  incluido integer;
  BEGIN
    IF (NEW.unico) THEN
      INSERT INTO "WebAccess_paquete" VALUES
      (DEFAULT,NEW.codserv,'Paquete ' || NEW.nombreserv,NEW.costo);
      INSERT INTO "WebAccess_contiene" VALUES
      (DEFAULT,NEW.codserv,NEW.codserv,1);
    END IF;
    RETURN NEW;
  END;  
$autoCreaPaquete$ LANGUAGE plpgsql;

CREATE TRIGGER autoCreaPaquete
AFTER INSERT ON "WebAccess_servicio" FOR EACH ROW 
EXECUTE PROCEDURE autoCreaPaquete();


CREATE OR REPLACE FUNCTION actualizaSaldo() 
RETURNS TRIGGER AS $actualizaSaldo$
DECLARE
    
  cantidad_incluida_paquete integer;
  cantidad_incluida_plan integer;
  cantidad_incluida_total integer;
  cantidad_incluida integer;
  cantidad_total_consumida integer;
  cantidad_consumida integer;
  costo_servicio double precision;
  costo_extra double precision;
  saldo_actual double precision;
  saldo_nuevo double precision;
    
  BEGIN
  
    
    IF EXISTS (SELECT *
               FROM "WebAccess_afilia"
               WHERE numserie_id = NEW.numserie_id) THEN RETURN NULL;
    END IF;
    
    cantidad_incluida_paquete := (SELECT cantidad
                                 FROM "WebAccess_contrata" NATURAL JOIN "WebAccess_contiene"
                                 WHERE numserie_id = NEW.numserie_id AND codserv_id = NEW.codserv_id);
                                 
    if cantidad_incluida_paquete is null then cantidad_incluida_paquete := 0; end if;
                                 
    cantidad_incluida_plan := (SELECT cantidad
                               FROM "WebAccess_activa" NATURAL JOIN "WebAccess_incluye"
                               WHERE numserie_id = NEW.numserie_id AND codserv_id = NEW.codserv_id);
    
    if cantidad_incluida_plan is null then cantidad_incluida_plan := 0; end if;
    
    cantidad_incluida := cantidad_incluida_paquete + cantidad_incluida_plan;
    
    
    SELECT SUM(cantidad) INTO cantidad_total_consumida
    FROM "WebAccess_consume"
    WHERE numserie_id = NEW.numserie_id AND codserv_id = NEW.codserv_id
        AND EXTRACT(month FROM fecha) = EXTRACT(month FROM NEW.fecha)
        AND EXTRACT(year FROM fecha) = EXTRACT(year FROM NEW.fecha);
    
    cantidad_consumida := NEW.cantidad;
    cantidad_total_consumida := cantidad_total_consumida - cantidad_consumida;
    cantidad_incluida_total := cantidad_incluida - cantidad_total_consumida;
        
    costo_servicio := (SELECT tarifa 
                       FROM "WebAccess_activa" NATURAL JOIN "WebAccess_incluye"
                       WHERE numserie_id = NEW.numserie_id AND codserv_id = NEW.codserv_id);

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
                     FROM "WebAccess_activa"
                     WHERE numserie_id = NEW.numserie_id);                     
                        
    saldo_nuevo := saldo_actual-costo_extra;
    
    UPDATE "WebAccess_activa"
    SET saldo = saldo_nuevo
    WHERE numserie_id = NEW.numserie_id;
    
    RETURN NEW;
    
  END;
$actualizaSaldo$ LANGUAGE plpgsql;

CREATE TRIGGER actualizaSaldo 
AFTER INSERT ON "WebAccess_consume" FOR EACH ROW 
EXECUTE PROCEDURE actualizaSaldo();


CREATE OR REPLACE FUNCTION realizaRecarga() 
RETURNS TRIGGER AS $realizaRecarga$
DECLARE 
  saldo_actual double precision;
  cantidad_total double precision;
  
  BEGIN
    
    IF EXISTS (SELECT *
               FROM "WebAccess_afilia"
               WHERE numserie_id = NEW.numserie_id) THEN RETURN NEW;
    
    ELSE
      
      saldo_actual := (SELECT saldo
                       FROM "WebAccess_activa"
                       WHERE numserie_id = NEW.numserie_id);

      cantidad_total := NEW.cantidad + saldo_actual; 
      
      UPDATE "WebAccess_activa"
      SET saldo = cantidad_total
      WHERE numserie_id = NEW.numserie_id;
    
    END IF;
    
    return NEW;

  END;
$realizaRecarga$ LANGUAGE plpgsql;

CREATE TRIGGER realizaRecarga
AFTER INSERT ON "WebAccess_recarga"
FOR EACH ROW EXECUTE PROCEDURE realizaRecarga();


CREATE OR REPLACE FUNCTION existePlan()
RETURNS TRIGGER AS $existePlan$
  BEGIN

    IF EXISTS (SELECT * 
               FROM "WebAccess_afilia"
               WHERE NEW.numserie_id = numserie_id) 
        OR

        EXISTS (SELECT * 
               FROM "WebAccess_activa"
               WHERE NEW.numserie_id = numserie_id)
               
        THEN RETURN NULL;
    END IF;
    RETURN NEW;
  END;
$existePlan$ LANGUAGE plpgsql;
  
CREATE TRIGGER existePlan1
BEFORE INSERT ON "WebAccess_activa" FOR EACH ROW 
EXECUTE PROCEDURE existePlan();

CREATE TRIGGER existePlan2
BEFORE INSERT ON "WebAccess_afilia" FOR EACH ROW 
EXECUTE PROCEDURE existePlan();