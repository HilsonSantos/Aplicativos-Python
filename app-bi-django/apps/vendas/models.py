from django.db import models




class DimSegmento(models.Model):
    segmento_id = models.IntegerField(
        db_column="nrosegmento",
        primary_key=True
    )
    segmento_descricao = models.TextField(db_column="descsegmento")

    class Meta:
        managed = False
        db_table = '"pbi"."carga_segmento"'

class DimRepresentante(models.Model):
    representante_id = models.IntegerField(
        db_column="nrorepresentante",
        primary_key=True
    )
    representante_nome = models.TextField(db_column="apelido")

    class Meta:
        managed = False
        db_table = '"pbi"."carga_representante"'

class FatVenda(models.Model):
    id = models.AutoField(db_column="id",primary_key=True)
    cliente_id = models.IntegerField(db_column="seqpessoa")
    segmento = models.ForeignKey(
        DimSegmento,
        db_column="nrosegmento",
        to_field="segmento_id",
        on_delete=models.DO_NOTHING,
        related_name="vendas",
    )
    representante = models.ForeignKey(
        DimRepresentante,
        db_column="nrorepresentante",
        to_field="representante_id",
        on_delete=models.DO_NOTHING,
        related_name="vendas",
    )
    data = models.DateField(db_column="dtavda")
    vendas_liquida = models.DecimalField(
        db_column="vlrvendaliquida",
        max_digits=18,
        decimal_places=2,
    )

    class Meta:
        managed = False
        db_table = '"pbi"."carga_abcdistribuicaobase"'