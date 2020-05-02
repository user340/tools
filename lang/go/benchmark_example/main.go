package main

import (
	"fmt"
	"math"
	"math/rand"
)

// MaxDataSize is maximam data size
const MaxDataSize int32 = 1000

func generateRandomData() []int32 {
	var i int32
	r := rand.New(rand.NewSource(99))
	data := make([]int32, MaxDataSize)

	for i = 0; i < MaxDataSize; i++ {
		data[i] = r.Int31()
	}

	return data
}

func sortData(data *[]int32, result *[]int) {
	for _, value := range *data {
		(*result)[value] = 1
	}
}

func showData(result *[]int) {
	for i, value := range *result {
		if value == 1 {
			fmt.Println(i)
		}
	}
}

func main() {
	data := generateRandomData()
	result := make([]int, math.MaxInt32+1)

	sortData(&data, &result)
	showData(&result)
}
