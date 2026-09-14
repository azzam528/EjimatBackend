from difflib import SequenceMatcher

from sqlalchemy.orm import Session

from app.models.kependudukan import Penduduk


class DuplicateDetectionService:

    @staticmethod
    def similarity(text1: str, text2: str):

        if not text1 or not text2:
            return 0

        return SequenceMatcher(
            None,
            text1.lower(),
            text2.lower()
        ).ratio()


    @staticmethod
    def check_penduduk(
        db: Session,
        nama: str,
        tanggal_lahir=None,
        tempat_lahir: str = None
    ):

        results = []

        penduduk_list = (
            db.query(Penduduk).all()
        )

        for penduduk in penduduk_list:

            score = 0

            # ======================
            # NAME SIMILARITY
            # ======================

            name_score = (
                DuplicateDetectionService.similarity(
                    nama,
                    penduduk.nama
                )
            )

            if name_score >= 0.8:
                score += 50


            # ======================
            # BIRTH DATE
            # ======================

            if (
                tanggal_lahir
                and penduduk.tanggal_lahir
                and tanggal_lahir
                == penduduk.tanggal_lahir
            ):
                score += 30


            # ======================
            # BIRTH PLACE
            # ======================

            if (
                tempat_lahir
                and penduduk.tempat_lahir
                and tempat_lahir.lower()
                == penduduk.tempat_lahir.lower()
            ):
                score += 20


            # ======================
            # POSSIBLE DUPLICATE
            # ======================

            if score >= 50:

                results.append({
                    "penduduk_id": str(
                        penduduk.id
                    ),
                    "nama": penduduk.nama,
                    "score": score,
                    "name_similarity": round(
                        name_score * 100,
                        2
                    )
                })

        return sorted(
            results,
            key=lambda x: x["score"],
            reverse=True
        )