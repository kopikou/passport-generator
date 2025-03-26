<script setup lang="ts">

import {onBeforeMount, ref, watch} from "vue";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {api} from "boot/axios";
import {useQuasar} from "quasar";
import _ from "lodash";

const generatorViewStore = useGeneratorViewStore();
const $q = useQuasar()

const {
  rpdData,
  activeRpdId,
  semestersData,
  interactiveMethods,
  additionalInfo,
  disabled,
} = storeToRefs(generatorViewStore)

const tab = ref<string>('')
const methods = ref<string>('')

async function saveMethods() {
  $q.loading.show()
  let r = await api.post(`/api/generator/${activeRpdId.value}/save-additional-info/`, {
    type: "interactiveMethods",
    value: {
      "interactiveMethods": methods.value
    }
  }).then((v) => {
    $q.notify({
      message: "Данные <span class='text-bold'>о структуре дисциплины</span> сохранены!",
      color: "secondary",
      position: "bottom",
      html: true,
    })
    let key = _.findKey(additionalInfo.value, (x) => x.id == v.data.id)
    _.set(additionalInfo.value, `[${key}].value.interactiveMethods`, methods.value)
  }, (rej) => {
    $q.notify({
      message: "Данные <span class='text-bold'>о структуре дисциплины</span> не сохранены!",
      color: "negative",
      position: "bottom",
      html: true,
    })
  })

  $q.loading.hide()
}

watch(semestersData, () => {
  tab.value = `${semestersData.value[0].num}`
})

watch(interactiveMethods, () => {
  methods.value = interactiveMethods.value[0]?.value['interactiveMethods']
})

onBeforeMount(() => {
  tab.value = `${semestersData.value[0]?.num}`
  methods.value = interactiveMethods.value[0]?.value['interactiveMethods']
})

</script>

<template>
  <div>
    <div style="width: 95%">
      <span class="text-h6 q-pl-lg">Структура дисциплины</span>
      <p>Количество академических часов, выделенных на дисциплину Базы данных. Данные автоматически получены их учебного
        плана.</p>
      <q-separator class="q-mt-md q-mb-md"/>
      <q-tabs
        v-model="tab"
        align="left"
        narrow-indicator
        class="q-mb-md"
      >
        <q-tab class="text-teal bg-grey-4" v-for="item in semestersData" :name="`${item.num}`"
               :label="`Семестр ${item.num}`"/>
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
                <div class="self-center full-width no-outline text-center">
                  <span v-if="item.lekc">{{ item.lekc }}</span>
                  <span v-else>Отсутствует</span>
                </div>
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

            <div class="text-subtitle1">Самостоятельные работы <span class="text-grey-6">(в том числе курсовое проектирование)</span>
            </div>
            <q-field outlined dense>
              <template v-slot:control>
                <div class="self-center full-width no-outline text-center">
                  <span v-if="item.srs">{{ item.srs }}</span>
                  <span v-else>Отсутствует</span>
                </div>
              </template>
            </q-field>

            <div class="text-subtitle1">Электронное информационная образовательная среда
            </div>
            <q-field outlined dense>
              <template v-slot:control>
                <div class="self-center full-width no-outline text-center">
                  <span v-if="item.eios">{{ item.eios }}</span>
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
                  <span v-if="!item.ekz && !item.zach && !item.zacho">Отсутствует</span>
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
      <div class="q-gutter-md">
        <div class="text-h6">
          Интерактивные методы обучения можно посмотреть по <a target="_blank" href="https://edu.itmo.ru/ru/edutech_iteractiv/">ссылке</a> или этой <a target="_blank" href="https://sberuniversity.ru/edutech-club/lab/glossary/937/">ссылке</a>
        </div>
        <q-input
          label="Интерактивные методы обучения"
          filled
          stack-label
          v-model="methods"
          clearable
          :readonly="disabled"
          @update:modelValue="saveMethods"
          debounce="1000"
        />
<!--        <q-btn-->
<!--          label="Сохранить"-->
<!--          color="primary"-->
<!--          @click="saveMethods"-->
<!--          v-show="!disabled"-->
<!--        />-->
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">

.structure-form {
  display: grid;
  grid-template-columns: 340px auto;
}

</style>
