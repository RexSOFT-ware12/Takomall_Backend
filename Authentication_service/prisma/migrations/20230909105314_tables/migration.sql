-- CreateTable
CREATE TABLE "User" (
    "id" SERIAL NOT NULL,
    "full_name" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "created_at" TIMESTAMP(3),
    "assess_level_id" INTEGER,
    "reset_token" TEXT,
    "reset_token_expiration" TIMESTAMP(3),
    "deleted" BOOLEAN NOT NULL DEFAULT false,

    CONSTRAINT "User_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Access_level" (
    "id" SERIAL NOT NULL,
    "role" TEXT NOT NULL,
    "permissions" JSONB NOT NULL,
    "deleted" BOOLEAN NOT NULL DEFAULT false,

    CONSTRAINT "Access_level_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "User" ADD CONSTRAINT "User_assess_level_id_fkey" FOREIGN KEY ("assess_level_id") REFERENCES "Access_level"("id") ON DELETE SET NULL ON UPDATE CASCADE;
