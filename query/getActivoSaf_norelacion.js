/**
 * Todos los activos que no tengan relación con la recolección realizada
 */
db.saf.aggregate([
  {
    $lookup: {
      from: "inventario",
      localField: "codigo",
      foreignField: "codigo_anterior",
      as: "registros_inventario"
    }
  },
  {
    $match: {
      "registros_inventario.0": { $exists: false }
    }
  },
  {
    $project: {
      codigo: 1,
      anterior: 1,
      grupo: 1,
      descripcion: 1,
      responsable: 1,
      total_registros: { $size: "$registros_inventario" }
    }
  },
  {
    $sort:{ responsable:1}
  }
])