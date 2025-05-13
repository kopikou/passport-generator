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
  // $q.loading.show({message: "Сохранение данных"})
  if (generatorViewStore.abortGetDataController)
    generatorViewStore.abortGetDataController.abort()

  tatInfo.value = [...((tatInfo.value || []).filter((x: any) => x.type != props.type)), {
    "about": about.value,
    "example": example.value,
    "great": great.value,
    "good": good.value,
    "satisfactorily": satisfactorily.value,
    "unsatisfactory": unsatisfactory.value,
    "title": props.title,
    "type": props.type,
  }];

  let r = await api.post(`/api/generator/${activeRpdId.value}/save-additional-info/`, {
    "type": 'tat',
    "value": tatInfo.value,
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
  const key = _.findKey(tatInfo.value, x => x.type == props.type)
  if (key) {
    about.value = _.get(_.find(tatInfo.value, x => x.type == props.type), 'about', '')
    great.value = _.get(_.find(tatInfo.value, x => x.type == props.type), 'great', '')
    good.value = _.get(_.find(tatInfo.value, x => x.type == props.type), 'good', '')
    satisfactorily.value = _.get(_.find(tatInfo.value, x => x.type == props.type), 'satisfactorily', '')
    unsatisfactory.value = _.get(_.find(tatInfo.value, x => x.type == props.type), 'unsatisfactory', '')
    example.value = _.get(_.find(tatInfo.value, x => x.type == props.type), 'example', '')
  }
})

</script>

<template>
  <q-expansion-item
    :label=props.title
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
            hint="Если Вам не нужен пример задания, оставьте поле пустым"
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
