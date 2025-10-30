"""
Service pour le traitement des données avec Ray Data
"""

from typing import Dict, List

import pandas as pd
import ray

# Initialiser Ray Data
ray.init(ignore_reinit_error=True)


class DataProcessingService:
    """Service pour traiter les données avec Ray Data"""

    async def process_csv_file(self, file_content) -> List[Dict]:
        """
        Traiter un fichier CSV avec Ray Data

        Args:
            file_content: Contenu du fichier CSV

        Returns:
            Liste des enregistrements traités
        """
        try:
            # Le file_content est déjà un BytesIO depuis la route
            # Créer un DataFrame pandas
            df = pd.read_csv(file_content, low_memory=False)

            # Filtrer les lignes avec des valeurs manquantes pour ARRIVAL_DELAY
            df = df[df["ARRIVAL_DELAY"].notna()]

            # Convertir en Ray Dataset pour traitement distribué
            dataset = ray.data.from_pandas([df])

            # Traiter les données avec Ray Data
            processed_data = dataset.map_batches(self._process_batch, batch_format="pandas")

            # Collecter les résultats
            results = []
            for batch in processed_data.iter_batches(batch_size=1000):
                results.extend(batch.to_dict("records"))

            return results

        except Exception as e:
            raise RuntimeError(f"Erreur lors du traitement des données: {str(e)}") from e

    def _process_batch(self, batch: pd.DataFrame) -> pd.DataFrame:
        """
        Traiter un batch de données

        Args:
            batch: DataFrame pandas du batch

        Returns:
            DataFrame traité
        """
        # Nettoyer et préparer les données
        # Supprimer les colonnes non nécessaires si besoin
        # Normaliser les valeurs, etc.

        # TODO: Implement the data processing logic

        return batch

    async def process_local_file(self, file_path: str) -> List[Dict]:
        """
        Traiter un fichier local avec Ray Data

        Args:
            file_path: Chemin vers le fichier CSV

        Returns:
            Liste des enregistrements traités
        """
        try:
            # Créer un Ray Dataset directement depuis le fichier
            dataset = ray.data.read_csv(file_path)

            # Filtrer les valeurs manquantes
            dataset = dataset.filter(lambda x: x.get("ARRIVAL_DELAY") is not None)

            # Traiter les données
            processed_data = dataset.map_batches(self._process_batch, batch_format="pandas")

            # Collecter les résultats
            results = []
            for batch in processed_data.iter_batches(batch_size=1000):
                results.extend(batch.to_dict("records"))

            return results

        except Exception as e:
            raise RuntimeError(f"Erreur lors du traitement du fichier: {str(e)}") from e
