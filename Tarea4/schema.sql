--******************************************************************************
--************************* CREACION DE TABLAS *********************************
--******************************************************************************

-- Se ha desarrollado un código de error para los Warnings que se emiten de la base de datos
-- Los códigos tienen la forma INVEXYY donde:
-- INVE es una abreviación para InnovaError, 
--
-- X es un número que representa la severidad del error, donde 0 es para triggers que mantienen la 
-- consistencia, y 1 para advertencias que no afectan las inserciones
--
-- YY Es un código único que se le asigna a cada error. Se presenta un diccionario para estos códigos
--
-- Severidad 0:
-- 01: No se puede agregar un consumo si no hay un plan o paquete que lo respalde
--

CREATE TYPE plantype AS ENUM ('infinito', 'paquete');
CREATE TYPE planmode AS ENUM ('prepago', 'postpago');

CREATE TABLE CLIENTE (
  cedula        integer         PRIMARY KEY,
  nombrecl      varchar(50)     NOT NULL,
  direccion     varchar(100)    NOT NULL
);

CREATE TABLE EMPRESA (
  RIF           integer         PRIMARY KEY,
  razón_social  varchar(50)     NOT NULL
);

CREATE TABLE PAQUETE (
  codpaq        integer         PRIMARY KEY,
  nombrepaq     varchar(50)     NOT NULL,
  precio        real            NOT NULL,
  CONSTRAINT precioPaquetePositivo CHECK (precio > 0)
);

CREATE TABLE PLAN (
  codplan       integer         PRIMARY KEY,
  nombreplan    varchar(50)     NOT NULL,
  descripción   varchar(100)    NOT NULL,
  renta_basica  real            NOT NULL,
  renta_ilimitada real          NOT NULL,
  tipo          planmode        NOT NULL
  CONSTRAINT rentaPostpagoPositiva CHECK (renta_basica > 0)
  CONSTRAINT rentaIlimitadaPostpagoPositiva CHECK (renta_ilimitada > 0)
);

CREATE TABLE PLAN_POSTPAGO (
  codplan       integer         PRIMARY KEY references PLAN(codplan)
);

CREATE TABLE PLAN_PREPAGO (
  codplan       integer         PRIMARY KEY references PLAN(codplan)
);

CREATE TABLE PRODUCTO (
  numserie      varchar(10)     PRIMARY KEY,
  nombreprod    varchar(50)     NOT NULL,
  RIF           integer         NOT NULL references EMPRESA(RIF),
  cedula        integer         references CLIENTE(cedula)
);

CREATE TABLE SERVICIO (
  codserv       integer         PRIMARY KEY,
  nombreserv    varchar(50)     NOT NULL,
  costo         real            NOT NULL,
  unico         boolean         NOT NULL DEFAULT FALSE,
  CONSTRAINT costoServicioPositivo CHECK (costo >= 0)
);

CREATE TABLE ACTIVA (
  numserie      varchar(20)     references PRODUCTO(numserie),
  codplan       integer         references PLAN_PREPAGO(codplan),
  saldo         real            NOT NULL,
  PRIMARY KEY (numserie, codplan),
  CONSTRAINT saldoPositivo CHECK (saldo >= 0)
);

CREATE TABLE AFILIA (
  numserie      varchar(20)     references PRODUCTO(numserie),
  codplan       integer         references PLAN_POSTPAGO(codplan),
  tipo_plan     plantype        NOT NULL,     
  PRIMARY KEY (numserie, codplan)
);


CREATE TABLE CONSUME (
  consumo_pkey  SERIAL          primary key,
  numserie      varchar(20)     references PRODUCTO(numserie),
  codserv       integer         references SERVICIO(codserv),
  fecha         timestamp            NOT NULL,
  cantidad      int             NOT NULL,
  CONSTRAINT cantidadConsumePositiva CHECK (cantidad > 0)
);

CREATE TABLE CONTIENE (
  codpaq        integer         references PAQUETE(codpaq),
  codserv       integer         references SERVICIO(codserv),
  cantidad	integer         NOT NULL,
  PRIMARY KEY (codpaq,codserv,cantidad),
  CONSTRAINT cantidadContienePositiva CHECK (cantidad > 0)
);

CREATE TABLE CONTRATA (
  numserie      varchar(20)     references PRODUCTO(numserie),
  codpaq        integer         references PAQUETE(codpaq),
  PRIMARY KEY (numserie,codpaq)
);

CREATE TABLE INCLUYE (
  codplan       integer         references PLAN(codplan),
  codserv       integer         references SERVICIO(codserv),
  tarifa        real,
  cantidad      integer         NOT NULL,          
  PRIMARY KEY (codplan,codserv),
  CONSTRAINT tarifaServicioIncluyePositiva CHECK (tarifa >= 0),
  CONSTRAINT cantidadServicioIncluyePositiva CHECK (cantidad > 0)
);



--******************************************************************************
--******************************** TRIGGERS ************************************
--******************************************************************************

/*
 * Trigger que se encarga de la primera restricción explícita:
 * 1. Un producto debe estar asociado a un plan prepago o a un plan postpago y
 * no a ambos.
 */
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
BEFORE INSERT OR UPDATE ON ACTIVA FOR EACH ROW 
EXECUTE PROCEDURE existePlanPostpago();
  
CREATE TRIGGER existePlanPostpago 
BEFORE INSERT OR UPDATE ON AFILIA FOR EACH ROW 
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
  costoServ real;
  saldoAf integer;
  canti integer;
  incluido integer;
  porpaquete integer;
  codigopl integer;
  BEGIN
    codigopl = (select codplan from activa where numserie = NEW.numserie);
    porpaquete = (select cantidad from paquete natural join contiene where
codserv=NEW.codserv);
    if porpaquete is null then porpaquete = 0; end if;
    
    canti = (select sum(cantidad) from consume where codserv=NEW.codserv and
numserie = NEW.numserie
    and
to_number(to_char(fecha,'MM'),'9999999')=to_number(to_char(NEW.fecha,'MM'),
'9999999') 
    and
to_number(to_char(fecha,'YYYY'),'9999999')=to_number(to_char(NEW.fecha,'YYYY'),
'9999999') );
    if canti is null then canti = 0; end if;
    
    incluido = (select cantidad from incluye where codserv = NEW.codserv and
codplan =
    codigopl);
    if incluido is null then incluido = 0; end if;
    
    costoServ = (select tarifa from incluye where codserv = NEW.codserv and codplan=codigopl);
    saldoAf = (select saldo from activa where numserie = NEW.numserie);
    if NEW.cantidad > (incluido+porpaquete-canti) THEN 
      update activa set saldo =
(saldoAf-(NEW.cantidad-incluido+canti))*costoServ where numserie = NEW.numserie;
     
    else
      return null;
    END if;
    return NEW;
    
  END;  
$actualizaSaldo$ LANGUAGE plpgsql;

CREATE TRIGGER actualizaSaldo 
AFTER INSERT ON CONSUME FOR EACH ROW 
EXECUTE PROCEDURE actualizaSaldo();


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
BEFORE INSERT OR UPDATE ON ACTIVA FOR EACH ROW 
EXECUTE PROCEDURE existePlan();

CREATE TRIGGER existePlan2
BEFORE INSERT OR UPDATE ON AFILIA FOR EACH ROW 
EXECUTE PROCEDURE existePlan();
