using System;
using System.Text;
using System.Threading.Tasks;
using HtmlAgilityPack;
using ScrapySharp.Extensions;
using Newtonsoft.Json;
using System.Net.Http;
using System.Net;

namespace complements
{
    class Program
    {
        private static string getImage(string nombre)
        {
            string imageUrl="";
            HtmlWeb oWeb = new HtmlWeb();
            WebClient oClient = new WebClient();
            HtmlAgilityPack.HtmlDocument doc;
            string url;
            url = "http://dixgamer.com/shop/juegos/ps4/accion-ps4/" + nombre.Replace(" ", "-") + "/?v=1d7b33fc26ca";
            doc = oWeb.Load(url);
            foreach (var Nodo in doc.DocumentNode.CssSelect("img.wp-post-image"))
            {
                imageUrl=Nodo.GetAttributeValue("src");
            }
            return imageUrl;
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
                game = game.Replace("-", " ");
            }
            else
            {
                game = "borderlands 3";
            }

            Console.WriteLine("Proceso Complements");

            string imgGame = getImage(game);

            Complement data = new Complement(game, imgGame);
            
            var json = JsonConvert.SerializeObject(new
            {
                type = "complements",
                date = DateTime.UtcNow.ToString("dd-MM-yyyy") + "$" + DateTime.Now.TimeOfDay,
                data = data
            });

            await SendJsonAsync(json);
            Console.WriteLine("Proceso exitoso!\n");
        }

        public static async Task SendJsonAsync(string json)
        {
            using (var client = new HttpClient())
            {
                var response = await client.PostAsync(
                    "https://young-harbor-56590.herokuapp.com/setComplements",
                     new StringContent(json, Encoding.UTF8, "application/json"));
            }
        }
    }
}
