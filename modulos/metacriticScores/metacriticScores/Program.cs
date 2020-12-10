using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;
using HtmlAgilityPack;
using ScrapySharp.Extensions;
using Newtonsoft.Json;
using System.Net.Http;
using System.Threading;

namespace metacriticScores
{
    class Program
    {

        public static Score getMetacriticScore(string nombre)
        {
            HtmlWeb oWeb = new HtmlWeb();
            string url;
            Score score;
            HtmlAgilityPack.HtmlDocument doc;
            List<Score> listaScores = new List<Score>();
            url = "https://www.metacritic.com/search/all/" + nombre + "/results";
            doc = oWeb.Load(url);

            score = null;
            foreach (var Nodo in doc.DocumentNode.CssSelect("span.metascore_w.medium.game"))
            {
                if (score == null)
                {
                    if (Nodo.InnerText != null && Nodo.InnerText != "tbd")
                    {
                        score = new Score(nombre.ToLower(),float.Parse("" + (10.0 * Int16.Parse(Nodo.InnerText)) / 100.0));
                        break;
                    }
                }
            }
            if (score == null)
            {
                score = new Score(nombre.ToLower(), 0);
                listaScores.Add(score);
            }
            return score;
        }

        static async Task Main(string[] args)
        {
             string game = "";

            if (args.Length > 0)
            {

                foreach (var arg in args)
                {
                    game = arg;
                }
                game=game.Replace("-", " ");
            }
            else
            {
                game = "borderlands 3";
            }

            Console.WriteLine("Proceso Metacritic");

            Score dataGame = getMetacriticScore(game);

            var json = JsonConvert.SerializeObject(new
            {
                type = "metacriticScore",
                date = DateTime.UtcNow.ToString("dd-MM-yyyy") + "$" + DateTime.Now.TimeOfDay,
                data = dataGame
            });

            await SendJsonAsync(json);
            Console.WriteLine("Proceso exitoso!\n");
        }

        public static async Task SendJsonAsync(string json)
        {
            using (var client = new HttpClient())
            {
                var response = await client.PostAsync(
                    "http://localhost:5000/setMetacritic",
                     new StringContent(json, Encoding.UTF8, "application/json"));
            }
        }
    }
}
