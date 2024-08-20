<script setup lang="ts">

import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";

const generatorViewStore = useGeneratorViewStore()

const {
  rpdData,
} = storeToRefs(generatorViewStore)

</script>

<template>
  <div>
    <div style="width: 95%">
      <span class="text-h6 q-pl-lg">Данные по дисциплине</span>
      <p>Данные для рабочей программы по дисциплине "Базы данных" получены автоматически из учебного плана</p>
      <q-separator class="q-mt-md q-mb-md"/>
      <div class="q-pb-md">
        <span class="text-subtitle1">Наименование дисциплины</span>
        <q-field outlined dense>
          <template v-slot:control>
            <div class="self-center full-width no-outline">asdfasds</div>
          </template>
        </q-field>
        <span class="text-subtitle1">Профиль/Специальность</span>
        <q-field outlined dense>
          <template v-slot:control>
            <div class="self-center full-width no-outline">asdfasds</div>
          </template>
        </q-field>
        <span class="text-subtitle1">Наименование направления</span>
        <q-field outlined dense>
          <template v-slot:control>
            <div class="self-center full-width no-outline">asdfasds</div>
          </template>
        </q-field>
        <span class="text-subtitle1">Кафедра</span>
        <q-field outlined dense>
          <template v-slot:control>
            <div class="self-center full-width no-outline">asdfasds</div>
          </template>
        </q-field>
      </div>
      <span class="text-h6 q-pl-lg">Данные о семестре</span>
      <q-separator class="q-mt-md q-mb-md"/>
      <div class="flex justify-center items-center">
        <span class="text-subtitle1">Количество семестров</span>
        <q-field filled dense style="width: 5%" class="q-ml-md q-mr-md">
          <template v-slot:control>
            <div class="self-center full-width no-outline text-center">2</div>
          </template>
        </q-field>
        <span class="text-subtitle1">Начальный семестр</span>
        <q-field filled dense style="width: 5%" class="q-ml-md">
          <template v-slot:control>
            <div class="self-center full-width no-outline text-center">4</div>
          </template>
        </q-field>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">

</style>
