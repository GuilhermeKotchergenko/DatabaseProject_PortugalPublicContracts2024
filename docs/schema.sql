CREATE TABLE ADJUDICANTE (
    NIFAdjudicante NUMBER (10)   PRIMARY KEY,
    designacao     VARCHAR (100) 
);

CREATE TABLE ADJUDICATARIO (
    ChaveAdjudicatario NUMBER (6)    PRIMARY KEY,
    NIFAdjudicatario   VARCHAR (50),
    designacao         VARCHAR (100) 
);

CREATE TABLE CONTRATOS (
    IdContrato               NUMBER (10)   PRIMARY KEY,
    TipoProcedimento         VARCHAR (20),
    ObjetivoContrato         VARCHAR (200),
    DataPublicacao           DATE,
    DataCelebracaoContrato   DATE,
    preco                    REAL (30),
    PrazoExecucao            VARCHAR (10), 
    Fundamentacao            VARCHAR (200),
    ProcedimentoCentralizado VARCHAR (10),
    DescrAcordoQuadro        VARCHAR (200),
    NIFAdjudicante           NUMBER (10)   REFERENCES ADJUDICANTE (NIFAdjudicante) 
);

CREATE TABLE PAIS (
    IdPais     NUMBER (2)   PRIMARY KEY,
    Designacao VARCHAR (20) 
);

CREATE TABLE DISTRITO (
    IdDistrito   NUMBER (2)   PRIMARY KEY,
    NomeDistrito VARCHAR (20) 
);

CREATE TABLE MUNICIPIO (
    IdMunicipio   NUMBER (3)   PRIMARY KEY,
    NomeMunicipio VARCHAR (30) 
);

CREATE TABLE CONTRATOSADJUDICATARIO (
    IdContrato         NUMBER (10) REFERENCES CONTRATOS (IdContrato),
    ChaveAdjudicatario NUMBER (6)  REFERENCES ADJUDICATARIO (ChaveAdjudicatario),
    PRIMARY KEY (
        IdContrato,
        ChaveAdjudicatario
    )
);

CREATE TABLE LOCALIZACAOCONTRATOS (
    ChaveLocalizacao NUMBER (6)  PRIMARY KEY,
    IdContrato       NUMBER (10) REFERENCES CONTRATOS (IdContrato),
    IdPais           NUMBER (2)  REFERENCES PAIS (IdPais),
    IdDistrito       NUMBER (2)  REFERENCES DISTRITO (IdDistrito),
    IdMunicipio      NUMBER (3)  REFERENCES MUNICIPIO (IdMunicipio) 
);

CREATE TABLE CPV (
    CodCpv     VARCHAR (12)  PRIMARY KEY,
    designacao VARCHAR (100) 
);

CREATE TABLE TIPOS (
    ChaveTipo NUMBER (2)    PRIMARY KEY,
    Tipo      VARCHAR (100) 
);

CREATE TABLE TIPODOCONTRATO (
    Idcontrato NUMBER (10) REFERENCES CONTRATOS (idContrato),
    ChaveTipo  NUMBER (2)  REFERENCES TIPOS (ChaveTipo),
    PRIMARY KEY (
        IdContrato,
        ChaveTipo
    )
);

CREATE TABLE CONTRATOSCPV (
    IdContrato NUMBER (10)  REFERENCES CONTRATOS (idContrato),
    CodCpv     VARCHAR (12) REFERENCES CPV (CodCPV),
    PRIMARY KEY (
        IdContrato,
        CodCpv
    )
);
