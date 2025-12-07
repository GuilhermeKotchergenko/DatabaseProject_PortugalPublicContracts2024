# Modelo Relacional:

CONTRATOS(	IdContrato,TipoContrato,TipoProcedimento,ObjetoContrato,DataPublicacao,DataCelebracaoContrato,Preco,PrazoExecucao,Fundamentacao,ProcedimentoCentralizado,DescrAcordoQuadro,idMunicipio→Municipio,CodCpv→Cpv,NIFAdjudicante→Adjudicante)

Cpv(CodCpv,Designacao)

Adjudicante(NIFAdjudicante,Designacao)

Adjudicatario(ChaveAdjudicatario,NIFAdjudicatario,Designacao)

Pais(IdPais,NomePais)

Distrito(IdDistrito,NomeDistrito,IdPais→Pais )

Municipio(IdMunicipio,NomeMunicipio,IdDistrito→Distrito)

LocalizacoesContratos(IdContrato→Contrato,IdMunicipio→Municipio) 

ContratosAdjudicatario(ChaveAdjudicatario→Adjudicatario,IdContrato→Contrato)


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
