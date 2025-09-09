db.inventario.aggregate([
  {
    $match: {
      codigo_anterior: { $ne: null, $exists: true },
      encargado: {
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
      from: "saf",
      localField: "codigo_anterior",
      foreignField: "codigo",
      as: "saf_relacionado"
    }
  },
  {
    $match: {
      "saf_relacionado": { $eq: [] }
    }
  },
  {
    $group: {
      _id: "$codigo_anterior",
      total_registros: { $sum: 1 },
      registros: {
        $push: {
          _id: "$_id",
          nro: "$nro",
          codigo_nuevo: "$codigo_nuevo",
          grupo: "$grupo",
          descripcion: "$descripcion",
          estado_uso_activo: "$estado_uso_activo",
          area: "$area",
          saf: "$saf",
          ubicacion: "$ubicacion",
          encargado: "$encargado",
          fecha_registro: "$fecha_registro"
        }
      }
    }
  },
  {
    $match: {
      total_registros: { $gte: 2 }
    }
  },
  {
    $sort: { total_registros: -1, _id: 1 }
  }
])