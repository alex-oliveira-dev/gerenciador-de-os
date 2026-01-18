# Repository para buscar carros em manutenção
from backend.database.database import Database


def listar_carros_em_manutencao():
    db = Database()
    rows = db.fetchall(
        """
        SELECT id, cliente, veiculo, defeito_relatado, status
        FROM ordens_servico
        WHERE status != 'Finalizada' AND status != 'Cancelada'
        """
    )
    return [
        {
            "id": row[0],
            "cliente": row[1],
            "veiculo": row[2],
            "defeito_relatado": row[3],
            "status": row[4],
        }
        for row in rows
    ]
