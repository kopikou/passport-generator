<script setup lang="ts">

import {useQuasar} from "quasar";
import {storeToRefs} from "pinia";
import useGeneratorViewStore from "stores/generatorViewStore";
import {onBeforeMount, ref, watch} from "vue";
import _ from "lodash";
import {api} from "boot/axios";

const generatorViewStore = useGeneratorViewStore();
const $q = useQuasar()
const {
  activeRpdId,
  additionalInfo,
  tatInfo,
  disabled,
} = storeToRefs(generatorViewStore)

const props = defineProps({
  title: {
    required: true,
  },
  type: {
    required: true,
  },
})

const main = ref('')
const about = ref('')
const example = ref('')

const great = ref('')
const good = ref('')
const satisfactorily = ref('')
const unsatisfactory = ref('')

async function saveData() {
  $q.loading.show({message: "Сохранение данных"})
  _.set(tatInfo.value, `[0].${props.type}`, {
    "main": main.value,
    "about": about.value,
    "example": example.value,
    "great": great.value,
    "good": good.value,
    "satisfactorily": satisfactorily.value,
    "unsatisfactory": unsatisfactory.value,
    "title": props.title,
  })
  let r = await api.post(`/api/generator/${activeRpdId.value}/save-additional-info/`, {
    "type": 'tat',
    "value": tatInfo.value,
  }).then((v) => {
    $q.notify({
      message: "Данные <span class='text-bold'>о типовых оценочных средствах</span> сохранены!",
      color: "secondary",
      position: "bottom",
      html: true,
    })
  }, (rej) => {
    $q.notify({
      message: "Данные <span class='text-bold'>о типовых оценочных средствах</span> не сохранены!",
      color: "negative",
      position: "bottom",
      html: true,
    })
  })
  $q.loading.hide()
}

watch(additionalInfo, () => {
  main.value = _.get(tatInfo.value, `[0].${props.type}.main`)
  about.value = _.get(tatInfo.value, `[0].${props.type}.about`)
  great.value = _.get(tatInfo.value, `[0].${props.type}.great`)
  good.value = _.get(tatInfo.value, `[0].${props.type}.good`)
  satisfactorily.value = _.get(tatInfo.value, `[0].${props.type}.satisfactorily`)
  unsatisfactory.value = _.get(tatInfo.value, `[0].${props.type}.unsatisfactory`)
  example.value = _.get(tatInfo.value, `[0].${props.type}.example`)
})

onBeforeMount(() => {
  main.value = _.get(tatInfo.value, `[0].${props.type}.main`)
  about.value = _.get(tatInfo.value, `[0].${props.type}.about`)
  great.value = _.get(tatInfo.value, `[0].${props.type}.great`)
  good.value = _.get(tatInfo.value, `[0].${props.type}.good`)
  satisfactorily.value = _.get(tatInfo.value, `[0].${props.type}.satisfactorily`)
  unsatisfactory.value = _.get(tatInfo.value, `[0].${props.type}.unsatisfactory`)
  example.value = _.get(tatInfo.value, `[0].${props.type}.example`)
})

</script>

<template>
  <q-expansion-item
    :label=props.title
  >
    <q-card>
      <q-card-section>
        <div class="q-gutter-md">
          <q-input
            label="Основная информация"
            type="textarea"
            filled
            stack-label
            v-model="main"
            :readonly="disabled"
            debounce="1000"
            @update:modelValue="saveData"
          />
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
            label="Пример билета"
            type="textarea"
            filled
            stack-label
            v-model="example"
            :readonly="disabled"
            debounce="1000"
            @update:modelValue="saveData"
            hint="Если Вам не нужен пример билета, оставьте поле пустым"
          />
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
