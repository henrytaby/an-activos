db.saf.aggregate([
  {
    $match: {
      responsable: {
        $nin: [
          "ZELADA GUARACHI RONALD",
          "URQUIDI SALMON JOSE PASTOR", 
          "RIOS JARAMILLO JORGE",
          "MIRANDA CHAVEZ MARISOL",
          "MENDIZABAL PACHECO AUGUSTO",
          "LIMA LLUSCO JULIO CESAR",
          "DIAZ CAMACHO ALISSON ALEJANDRA",
          "ABAN ARAMAYO OMAR"
        ]
      }
    }
  },
  {
    $lookup: {
      from: "inventario",
      localField: "codigo",
      foreignField: "codigo_anterior",
      as: "registros_inventario"
    }
  },
  {
    $project: {
      codigo: 1,
      anterior: 1,
      grupo: 1,
      descripcion: 1,
      estadousoactivo: 1,
      estadoactivo: 1,
      proyecto: 1,
      responsable: 1,
      fecha_registro: 1,
      total_registros: { $size: "$registros_inventario" },
      registros_inventario: {
        $map: {
          input: "$registros_inventario",
          as: "reg",
          in: {
            nro: "$$reg.nro",
            codigo_nuevo: "$$reg.codigo_nuevo",
            estado_uso_activo: "$$reg.estado_uso_activo",
            area: "$$reg.area",
            ubicacion: "$$reg.ubicacion",
            encargado: "$$reg.encargado"
          }
        }
      }
    }
  },
  {
    $sort: { total_registros: 1, responsable: -1, codigo: 1 }
  }
])