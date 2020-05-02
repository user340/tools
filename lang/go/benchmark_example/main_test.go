package main

import (
	"math"
	"testing"
)

func BenchmarkRandomData(b *testing.B) {
	generateRandomData()
}

func BenchmarkSortData(b *testing.B) {
	data := generateRandomData()
	result := make([]int, math.MaxInt32+1)

	sortData(&data, &result)
}
