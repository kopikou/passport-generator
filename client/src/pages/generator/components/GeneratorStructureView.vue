<script setup lang="ts">

import {ref} from "vue";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";

const generatorViewStore = useGeneratorViewStore();

const{
  semestersData,
}=storeToRefs(generatorViewStore)

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
        <q-tab class="text-teal bg-grey-4"  v-for="item in semestersData" :name="`${item.num}`" :label="`${item.num}`"/>
      </q-tabs>

      <q-tab-panels
          v-model="tab"
          animated
          transition-prev="scale"
          transition-next="scale"
      >
        <q-tab-panel v-for="item in semestersData" :name="`${item.num}`">
          <div class="structure-form q-gutter-md">
            <div class="text-subtitle1">Лекции</div>
            <q-field outlined dense>
              <template v-slot:control>
                <div class="self-center full-width no-outline text-center">{{ item.num }}</div>
              </template>
            </q-field>

            <div class="text-subtitle1">Лабораторные</div>
            <q-field outlined dense>
              <template v-slot:control>
                <div class="self-center full-width no-outline text-center">
                  <span v-if="item.lab">{{ item.lab }}</span>
                  <span v-else>Отсутствует</span>
                </div>
              </template>
            </q-field>

            <div class="text-subtitle1">Практики/Семинары</div>
            <q-field outlined dense>
              <template v-slot:control>
                <div class="self-center full-width no-outline text-center">
                  <span v-if="item.pr">{{ item.pr }}</span>
                  <span v-else>Отсутствует</span>
                </div>
              </template>
            </q-field>

            <div class="text-subtitle1">Самостоятельные работы <span class="text-grey-6">(в том числе курсовое проектирование)</span></div>
            <q-field outlined dense>
              <template v-slot:control>
                <div class="self-center full-width no-outline text-center">
                  <span v-if="item.srs">{{ item.srs }}</span>
                  <span v-else>Отсутствует</span>
                </div>
              </template>
            </q-field>

            <div class="text-subtitle1">Трудоемкость промежуточной аттестации</div>
            <q-field outlined dense>
              <template v-slot:control>
                <div class="self-center full-width no-outline text-center">
                  <span v-if="item.ekzhour">{{ item.ekzhour }}</span>
                  <span v-else>Отсутствует</span>
                </div>
              </template>
            </q-field>

            <div class="text-subtitle1">ЗЕТ</div>
            <q-field outlined dense>
              <template v-slot:control>
                <div class="self-center full-width no-outline text-center">
                  <span v-if="item.zet">{{ item.zet }}</span>
                  <span v-else>Отсутствует</span>
                </div>
              </template>
            </q-field>

            <div class="text-subtitle1">Вид промежуточной аттестации</div>
            <q-field outlined dense>
              <template v-slot:control>
                <div class="self-center full-width no-outline text-center">
                  <span v-if="item.ekz">Экзамен</span>
                  <span v-if="item.zach">Зачет</span>
                  <span v-if="item.zacho">Зачет с оценкой></span>
                </div>
              </template>
            </q-field>

            <div class="text-subtitle1">Курсовой проект/курсовая работа</div>
            <q-field outlined dense>
              <template v-slot:control>
                <div class="self-center full-width no-outline text-center">
                  <span v-if="item.kr">Курсовая работа</span>
                  <span v-else-if="item.kp">Курсовой проект</span>
                  <span v-else-if="item.kp && item.kr">Курсовой проект и курсовая работа</span>
                  <span v-else>Отсутствует</span>
                </div>
              </template>
            </q-field>
          </div>
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
