<script setup lang="ts">

import {useQuasar} from "quasar";
import {storeToRefs} from "pinia";
import useGeneratorViewStore from "stores/generatorViewStore";
import {onBeforeMount, ref, watch, watchEffect} from "vue";
import _ from "lodash";
import {api} from "boot/axios";

const generatorViewStore = useGeneratorViewStore();
const $q = useQuasar()
const {
  activeRpdId,
  additionalInfo,
  tatInfo,
  disabled,
  planlinesData,
  semesterYearLabel,
} = storeToRefs(generatorViewStore)

const props = defineProps({
  title: {
    required: true,
  },
  type: {
    required: true,
  },
  num: {
    required: true,
  }
})

const main = ref('')
const about = ref('')
const example = ref('')

const great = ref('')
const good = ref('')
const satisfactorily = ref('')
const unsatisfactory = ref('')

const tat = ref('')
const form = ref('')
const formabout = ref('')

async function saveData() {
  // $q.loading.show({message: "Сохранение данных"})
  if (generatorViewStore.abortGetDataController)
    generatorViewStore.abortGetDataController.abort()


  let res = {
      "great": great.value,
      "good": good.value,
      "satisfactorily": satisfactorily.value,
      "unsatisfactory": unsatisfactory.value,
      "title": props.title,
      "type": props.type,
      "num": props.num,
  }
  if (planlinesData.value.viewpract) {
    res = {
      ...res,
      "tat": tat.value,
      "form": form.value,
      "formabout": formabout.value,
    }
  } else {
    res = {
      ...res,
      "about": about.value,
      "example": example.value,
    }
  }

  const data = [...((tatInfo.value || []).filter((x: any) => x.type != props.type)), res]

  let r = await api.post(`/api/generator/${activeRpdId.value}/save-additional-info/`, {
    "type": 'tat',
    "value": data,
  })
  $q.notify({
    message: "Данные <span class='text-bold'>о типовых оценочных средствах</span> сохранены!",
    color: "secondary",
    position: "bottom",
    html: true,
  })
  await generatorViewStore.getData()
  generatorViewStore.checkErrors()

  $q.loading.hide()
}

watchEffect(() => {
  const data = _.find(tatInfo.value, x => x.type == props.type && x.num == props.num)
  if (data) {
    about.value = _.get(data, 'about', '')
    great.value = _.get(data, 'great', '')
    good.value = _.get(data, 'good', '')
    satisfactorily.value = _.get(data, 'satisfactorily', '')
    unsatisfactory.value = _.get(data, 'unsatisfactory', '')
    example.value = _.get(data, 'example', '')
    tat.value = _.get(data, 'tat', '')
    form.value = _.get(data, 'form', '')
    formabout.value = _.get(data, 'formabout', '')
  }
})

</script>

<template>
  <q-expansion-item
    :label="`${semesterYearLabel} ${props.num} | ${props.title}`"
  >
    <q-card>
      <q-card-section>
        <div class="q-gutter-md">
          <!--          <q-input-->
          <!--            label="Основная информация"-->
          <!--            type="textarea"-->
          <!--            filled-->
          <!--            stack-label-->
          <!--            v-model="main"-->
          <!--            :readonly="disabled"-->
          <!--            debounce="1000"-->
          <!--            @update:modelValue="saveData"-->
          <!--          />-->
          <div class="q-gutter-y-md" v-if="!planlinesData.viewpract">
            <q-input
            label="Описание процедуры"
            type="textarea"
            filled
            stack-label
            v-model="about"
            :readonly="disabled"
            debounce="1000"
            @update:modelValue="saveData"
          />
          <q-input
            label="Пример задания"
            type="textarea"
            filled
            stack-label
            v-model="example"
            :readonly="disabled"
            debounce="1000"
            @update:modelValue="saveData"
          /></div>
          <div class="q-gutter-y-md" v-else>
            <q-input
              label="Типовые оценочные средства"
              type="text"
              filled
              stack-label
              v-model="tat"
              :debounce="1000"
              @update:modelValue="saveData"
            />
            <q-input
              label="Форма проведения зачета"
              type="text"
              filled
              stack-label
              v-model="form"
              :debounce="1000"
              @update:modelValue="saveData"
            />
            <q-input
              label="Описание процедуры проведения зачета"
              type="textarea"
              filled
              stack-label
              v-model="formabout"
              :debounce="1000"
              @update:modelValue="saveData"
            />
          </div>
          <p class="text-subtitle1">Критерии оценивания</p>
          <q-list bordered>
            <q-expansion-item
              label="Отлично"
            >
              <q-input
                class="q-pa-sm"
                label="Отлично"
                type="textarea"
                filled
                stack-label
                v-model="great"
                :readonly="disabled"
                debounce="1000"
                @update:modelValue="saveData"
              />
            </q-expansion-item>
            <q-expansion-item label="Хорошо">
              <q-input
                class="q-pa-sm"
                label="Хорошо"
                type="textarea"
                filled
                stack-label
                v-model="good"
                :readonly="disabled"
                debounce="1000"
                @update:modelValue="saveData"
              />
            </q-expansion-item>
            <q-expansion-item label="Удовлетворительно">
              <q-input
                class="q-pa-sm"
                label="Удовлетворительно"
                type="textarea"
                filled
                stack-label
                v-model="satisfactorily"
                debounce="1000"
                @update:modelValue="saveData"
              />
            </q-expansion-item>
            <q-expansion-item label="Неудовлетворительно">
              <q-input
                class="q-pa-sm"
                label="Неудовлетворительно"
                type="textarea"
                filled
                stack-label
                v-model="unsatisfactory"
                :readonly="disabled"
                debounce="1000"
                @update:modelValue="saveData"
              />
            </q-expansion-item>
          </q-list>
          <!--          <q-btn-->
          <!--            label="Сохранить"-->
          <!--            color="primary"-->
          <!--            @click="saveData"-->
          <!--            v-show="!disabled"-->
          <!--          />-->
        </div>
      </q-card-section>
    </q-card>
  </q-expansion-item>
  <q-separator/>
</template>

<style scoped>
</style>
