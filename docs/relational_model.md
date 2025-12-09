# Modelo Relacional:

CONTRATOS(	IdContrato,TipoProcedimento,ObjetoContrato,DataPublicacao,DataCelebracaoContrato,Preco,PrazoExecucao,Fundamentacao,ProcedimentoCentralizado,DescrAcordoQuadro,NIFAdjudicante→Adjudicante)

TIPOS(ChaveTipo,Designacao)

TIPOCONTRATOS(ChaveTipo→Tipo,IdContrato→Contrato)

CPV(CodCpv,Designacao)

CPVCONTRATOS(CodCpv → Cpv, IdContrato→Contrato)

ADJUDICANTE(NIFAdjudicante,Designacao)

ADJUDICATARIO(ChaveAdjudicatario,NIFAdjudicatario,Designacao)

PAIS(IdPais,NomePais)

DISTRITO(IdDistrito,NomeDistrito)

MUNICIPIO(IdMunicipio,NomeMunicipio)

LOCALIZACAOCONTRATOS(ChaveLocalizacao,IdContrato→Contrato,IdMunicipio→Municipio,IdDistrito→Distrito,IdPais→Pais) 

CONTRATOSADJUDICATARIO(ChaveAdjudicatario→Adjudicatario,IdContrato→Contrato)



# Código Dbdia:
table CONTRATOS
(
  _ IdContrato _,
  TipoContrato,
  TipoProcedimento,
  ObjetoContrato,
  DataPublicacao,
  DataCelebracaoContrato,
  Preco,
  PrazoExecucao,
  Fundamentacao,
  ProcedimentoCentralizado,
  DescrAcordoQuadro,
  IdMunicipio --> MUNICIPIO.IdMunicipio,
  CodCpv --> CPV.CodCpv,
  NIFAdjudicante --> ADJUDICANTE.NIFAdjudicante

)

table CPV
(
  _ CodCpv_ ,
  Designacao 
)

table ADJUDICANTE
(
  _ NIFAdjudicante_,
  Designacao
)

table ADJUDICATARIO
( 
  _ ChaveAdjudicatario_,
  NIFAdjudicatario,
  Designacao
)

table PAIS
(
  _ IdPais_ ,
  NomePais
)

table DISTRITO
(
  _ IdDistrito_ ,
  NomeDistrito ,
  idPais--> PAIS.IdPais
  
)

table MUNICIPIO
(
  _ IdMunicipio _,
  NomeMunicipio ,
  idDistrito--> DISTRITO.IdDistrito
  
)

table LOCALIZACAO_CONTRATO
(
  _ IdContrato _ --> CONTRATOS.IdContrato,
  _ IdMunicipio _ --> MUNICIPIO.IdMunicipio  
  
)

table CONTRATOS_ADJUDICATARIO
(
  _ ChaveAdjudicatario_ --> ADJUDICATARIO.ChaveAdjudicatario,
  _IdContrato_ --> CONTRATOS.IdContrato  
  
)
