BEGIN;
CREATE TABLE "WebAccess_cliente" (
    "id" serial NOT NULL PRIMARY KEY,
    "cedula" integer CHECK ("cedula" >= 0) NOT NULL UNIQUE,
    "nombrecl" varchar(50) NOT NULL,
    "direccion" text NOT NULL
)
;
CREATE TABLE "WebAccess_usuario" (
    "id" serial NOT NULL PRIMARY KEY,
    "cedula_id" integer NOT NULL REFERENCES "WebAccess_cliente" ("id") DEFERRABLE INITIALLY DEFERRED,
    "password" varchar(12) NOT NULL
)
;
CREATE TABLE "WebAccess_empresa" (
    "id" serial NOT NULL PRIMARY KEY,
    "RIF" integer CHECK ("RIF" >= 0) NOT NULL UNIQUE,
    "razon_social" varchar(50) NOT NULL
)
;
CREATE TABLE "WebAccess_paquete" (
    "id" serial NOT NULL PRIMARY KEY,
    "codpaq" integer CHECK ("codpaq" >= 0) NOT NULL UNIQUE,
    "nombrepaq" varchar(50) NOT NULL,
    "precio" double precision NOT NULL
)
;
CREATE TABLE "WebAccess_planpostpago" (
    "id" serial NOT NULL PRIMARY KEY,
    "codplan_id" integer NOT NULL
)
;
CREATE TABLE "WebAccess_planprepago" (
    "id" serial NOT NULL PRIMARY KEY,
    "codplan_id" integer NOT NULL
)
;
CREATE TABLE "WebAccess_plan" (
    "id" serial NOT NULL PRIMARY KEY,
    "codplan" integer CHECK ("codplan" >= 0) NOT NULL UNIQUE,
    "nombreplan" varchar(50) NOT NULL,
    "descripcion" text NOT NULL,
    "renta_basica" double precision NOT NULL,
    "renta_ilimitada" double precision NOT NULL,
    "tipo" varchar(8) NOT NULL
)
;
ALTER TABLE "WebAccess_planpostpago" ADD CONSTRAINT "codplan_id_refs_id_97a69192" FOREIGN KEY ("codplan_id") REFERENCES "WebAccess_plan" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "WebAccess_planprepago" ADD CONSTRAINT "codplan_id_refs_id_3ca5749d" FOREIGN KEY ("codplan_id") REFERENCES "WebAccess_plan" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE TABLE "WebAccess_producto" (
    "id" serial NOT NULL PRIMARY KEY,
    "numserie" varchar(10) NOT NULL UNIQUE,
    "nombreprod" varchar(50) NOT NULL,
    "RIF_id" integer NOT NULL REFERENCES "WebAccess_empresa" ("id") DEFERRABLE INITIALLY DEFERRED,
    "cedula_id" integer NOT NULL REFERENCES "WebAccess_cliente" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "WebAccess_activa" (
    "id" serial NOT NULL PRIMARY KEY,
    "codplan_id" integer NOT NULL REFERENCES "WebAccess_planprepago" ("id") DEFERRABLE INITIALLY DEFERRED,
    "numserie_id" integer NOT NULL REFERENCES "WebAccess_producto" ("id") DEFERRABLE INITIALLY DEFERRED,
    "saldo" double precision NOT NULL
)
;
CREATE TABLE "WebAccess_afilia" (
    "id" serial NOT NULL PRIMARY KEY,
    "codplan_id" integer NOT NULL REFERENCES "WebAccess_planpostpago" ("id") DEFERRABLE INITIALLY DEFERRED,
    "numserie_id" integer NOT NULL REFERENCES "WebAccess_producto" ("id") DEFERRABLE INITIALLY DEFERRED,
    "tipoplan" varchar(8) NOT NULL
)
;
CREATE TABLE "WebAccess_servicio" (
    "id" serial NOT NULL PRIMARY KEY,
    "codserv" integer CHECK ("codserv" >= 0) NOT NULL UNIQUE,
    "nombreserv" varchar(50) NOT NULL,
    "costo" double precision NOT NULL,
    "unico" boolean NOT NULL
)
;
CREATE TABLE "WebAccess_consume" (
    "id" serial NOT NULL PRIMARY KEY,
    "numserie_id" integer NOT NULL REFERENCES "WebAccess_producto" ("id") DEFERRABLE INITIALLY DEFERRED,
    "codserv_id" integer NOT NULL REFERENCES "WebAccess_servicio" ("id") DEFERRABLE INITIALLY DEFERRED,
    "fecha" timestamp with time zone NOT NULL,
    "cantidad" integer CHECK ("cantidad" >= 0) NOT NULL
)
;
CREATE TABLE "WebAccess_contiene" (
    "id" serial NOT NULL PRIMARY KEY,
    "codpaq_id" integer NOT NULL REFERENCES "WebAccess_paquete" ("id") DEFERRABLE INITIALLY DEFERRED,
    "codserv_id" integer NOT NULL REFERENCES "WebAccess_servicio" ("id") DEFERRABLE INITIALLY DEFERRED,
    "cantidad" integer CHECK ("cantidad" >= 0) NOT NULL
)
;
CREATE TABLE "WebAccess_contrata" (
    "id" serial NOT NULL PRIMARY KEY,
    "numserie_id" integer NOT NULL REFERENCES "WebAccess_producto" ("id") DEFERRABLE INITIALLY DEFERRED,
    "codpaq_id" integer NOT NULL REFERENCES "WebAccess_paquete" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "WebAccess_incluye" (
    "id" serial NOT NULL PRIMARY KEY,
    "codplan_id" integer NOT NULL REFERENCES "WebAccess_plan" ("id") DEFERRABLE INITIALLY DEFERRED,
    "codserv_id" integer NOT NULL REFERENCES "WebAccess_servicio" ("id") DEFERRABLE INITIALLY DEFERRED,
    "cantidad" integer CHECK ("cantidad" >= 0) NOT NULL,
    "tarifa" double precision NOT NULL
)
;
CREATE TABLE "WebAccess_recarga" (
    "id" serial NOT NULL PRIMARY KEY,
    "numserie_id" integer NOT NULL REFERENCES "WebAccess_producto" ("id") DEFERRABLE INITIALLY DEFERRED,
    "fecha" timestamp with time zone NOT NULL,
    "cantidad" integer CHECK ("cantidad" >= 0) NOT NULL
)
;

COMMIT;
