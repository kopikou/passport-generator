<script setup lang="ts">

import {ref} from "vue";

const tab = ref(null)

</script>

<template>
  <div>
    <div style="width: 95%">
      <span class="text-h6 q-pl-lg">Структура дисциплины "Базы данных"</span>
      <p>Количество академических часов, выделенных на дисциплину Базы данных. Данные автоматически получены их учебного
        плана.</p>
      <q-separator class="q-mt-md q-mb-md"/>
      <q-tabs
          v-model="tab"
          align="left"
          narrow-indicator
          class="q-mb-md"
      >
        <q-tab class="text-teal bg-grey-4" name="1" label="1"/>
        <q-tab class="text-teal bg-grey-4" name="2" label="2"/>
      </q-tabs>

      <q-tab-panels
          v-model="tab"
          animated
          transition-prev="scale"
          transition-next="scale"
      >
        <q-tab-panel name="1">
          <div class="structure-form q-gutter-md">
            <div class="text-subtitle1">Лекции</div>
            <q-field outlined dense>
              <template v-slot:control>
                <div class="self-center full-width no-outline text-center">12</div>
              </template>
            </q-field>

            <div class="text-subtitle1">Лабораторные</div>
            <q-field outlined dense>
              <template v-slot:control>
                <div class="self-center full-width no-outline text-center">4</div>
              </template>
            </q-field>

            <div class="text-subtitle1">Практики/Семинары</div>
            <q-field outlined dense>
              <template v-slot:control>
                <div class="self-center full-width no-outline text-center">4</div>
              </template>
            </q-field>

            <div class="text-subtitle1">Самостоятельные работы <span class="text-grey-6">(в том числе курсовое проектирование)</span></div>
            <q-field outlined dense>
              <template v-slot:control>
                <div class="self-center full-width no-outline text-center">4</div>
              </template>
            </q-field>

            <div class="text-subtitle1">Трудоемкость промежуточной аттестации</div>
            <q-field outlined dense>
              <template v-slot:control>
                <div class="self-center full-width no-outline text-center">4</div>
              </template>
            </q-field>

            <div class="text-subtitle1">ЗЕТ</div>
            <q-field outlined dense>
              <template v-slot:control>
                <div class="self-center full-width no-outline text-center">2</div>
              </template>
            </q-field>

            <div class="text-subtitle1">Вид промежуточной аттестации</div>
            <q-field outlined dense>
              <template v-slot:control>
                <div class="self-center full-width no-outline text-center">Экзамен</div>
              </template>
            </q-field>

            <div class="text-subtitle1">Курсовой проект/курсовая работа</div>
            <q-field outlined dense>
              <template v-slot:control>
                <div class="self-center full-width no-outline text-center">Курсовая работа</div>
              </template>
            </q-field>
          </div>
        </q-tab-panel>
        <q-tab-panel name="2">
          asdfasd
        </q-tab-panel>
      </q-tab-panels>
    </div>
  </div>
</template>

<style scoped lang="scss">

.structure-form {
  display: grid;
  grid-template-columns: 340px auto;
}

</style>
