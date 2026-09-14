import re

from difflib import SequenceMatcher

from sqlalchemy.orm import Session

from app.models.kependudukan import Penduduk


class DuplicateDetectionService:

    @staticmethod
    def normalize_text(value: str | None) -> str:

        if not value:
            return ""

        value = value.lower().strip()

        value = re.sub(
            r"[^a-z0-9\s]",
            "",
            value
        )

        value = re.sub(
            r"\s+",
            " ",
            value
        )

        return value


    @staticmethod
    def similarity(
        text1: str | None,
        text2: str | None
    ) -> float:

        text1 = (
            DuplicateDetectionService
            .normalize_text(text1)
        )

        text2 = (
            DuplicateDetectionService
            .normalize_text(text2)
        )

        if not text1 or not text2:
            return 0

        return SequenceMatcher(
            None,
            text1,
            text2
        ).ratio()


    @staticmethod
    def check_penduduk(
        db: Session,
        repository,
        data
    ):

        results = []

        penduduk_list = (
            repository.get_all_for_duplicate_check(db)
        )

        for penduduk in penduduk_list:

            score = 0

            # =========================
            # NAME SIMILARITY
            # =========================

            name_similarity = (
                DuplicateDetectionService.similarity(
                    data.nama_lengkap,
                    penduduk.nama_lengkap
                )
            )

            if name_similarity >= 0.90:

                score += 50

            elif name_similarity >= 0.80:

                score += 40


            # =========================
            # TANGGAL LAHIR
            # =========================

            if (
                hasattr(data, "tanggal_lahir")
                and data.tanggal_lahir
                and penduduk.tanggal_lahir
                and data.tanggal_lahir
                == penduduk.tanggal_lahir
            ):

                score += 30


            # =========================
            # TEMPAT LAHIR
            # =========================

            if (
                hasattr(data, "tempat_lahir")
                and data.tempat_lahir
                and penduduk.tempat_lahir
                and DuplicateDetectionService
                .normalize_text(data.tempat_lahir)
                ==
                DuplicateDetectionService
                .normalize_text(penduduk.tempat_lahir)
            ):

                score += 20


            # =========================
            # HASIL
            # =========================

            if score >= 50:

                results.append({

                    "penduduk_id": str(
                        penduduk.id
                    ),

                    "nik": penduduk.nik,

                    "nama_lengkap":
                        penduduk.nama_lengkap,

                    "similarity_score":
                        score,

                    "name_similarity":
                        round(
                            name_similarity * 100,
                            2
                        )

                })

        return sorted(
            results,
            key=lambda item:
                item["similarity_score"],
            reverse=True
        )