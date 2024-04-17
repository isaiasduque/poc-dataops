CREATE  TABLE IF NOT EXISTS raw_sales.tb_currency(
    fecha STRING,
    moneda STRING,
    compra FLOAT64,
    venta FLOAT64,
    origen STRING,
    process_datetime STRING
)