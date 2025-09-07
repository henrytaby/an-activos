/**
 * Agrupa todos los grupos y muestra cuantos registros se tiene para cada uno de ellos
 */
db.inventario.aggregate([
  {
    $group: {
      _id: "$grupo",
      total_registros: { $sum: 1 }
    }
  },
  {
    $sort: { _id: 1 }
  }
])