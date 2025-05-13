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
} = storeToRefs(generatorViewStore)

const props = defineProps({
  title: {
    required: true,
  },
  type: {
    required: true,
  }
})

const main = ref('')
const about = ref('')
const example = ref('')

const passed = ref('')
const unpassed = ref('')

const tat = ref('')
const form = ref('')
const formabout = ref('')

async function saveData() {
  // $q.loading.show({message: "Сохранение данных"})
  const key = _.findKey(tatInfo.value, x => x.type == props.type)

  let data = {}
  if (planlinesData.value.viewpract) {
    data = {
      "tat": tat.value,
      "form": form.value,
      "formabout": formabout.value,
      "passed": passed.value,
      "unpassed": unpassed.value,
      "title": props.title,
      "type": props.type,
    }
  } else {
    data = {
      "about": about.value,
      "example": example.value,
      "passed": passed.value,
      "unpassed": unpassed.value,
      "title": props.title,
      "type": props.type,
    }
  }

  if (!key) {
    tatInfo.value.push(data)
  } else {
    _.set(tatInfo.value, `[${key}]`, data)
  }

  let r = await api.post(`/api/generator/${activeRpdId.value}/save-additional-info/`, {
    "type": 'tat',
    "value": tatInfo.value,
  })

  if (r.status == 200) {
    $q.notify({
      message: "Данные <span class='text-bold'>о типовых оценочных средствах</span> сохранены!",
      color: "secondary",
      position: "bottom",
      html: true,
    })
    generatorViewStore.checkErrors()
  } else {
    $q.notify({
      message: "Данные <span class='text-bold'>о типовых оценочных средствах</span> не сохранены!",
      color: "negative",
      position: "bottom",
      html: true,
    })
  }
  // $q.loading.hide()
}

watchEffect(() => {
  const key = _.findKey(tatInfo.value, x => x.type == props.type)
  if (key) {
    about.value = _.get(_.find(tatInfo.value, x => x.type == props.type), 'about', '')
    passed.value = _.get(_.find(tatInfo.value, x => x.type == props.type), 'passed', '')
    unpassed.value = _.get(_.find(tatInfo.value, x => x.type == props.type), 'unpassed', '')
    example.value = _.get(_.find(tatInfo.value, x => x.type == props.type), 'example', '')
    tat.value = _.get(_.find(tatInfo.value, x => x.type == props.type), 'tat', '')
    form.value = _.get(_.find(tatInfo.value, x => x.type == props.type), 'form', '')
    formabout.value = _.get(_.find(tatInfo.value, x => x.type == props.type), 'formabout', '')
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
            />a
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
          </div>
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
              label="Зачтено"
            >
              <q-input
                class="q-pa-sm"
                label="Зачтено"
                type="textarea"
                filled
                stack-label
                v-model="passed"
                :readonly="disabled"
                debounce="1000"
                @update:modelValue="saveData"
              />
            </q-expansion-item>

            <q-expansion-item
              label="Не зачтено"
            >
              <q-input
                class="q-pa-sm"
                label="Не зачтено"
                type="textarea"
                filled
                stack-label
                v-model="unpassed"
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
